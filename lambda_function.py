# # import sys
# # import subprocess
# # import io

# # def execute_python_code(code):
# #     original_stdout = sys.stdout
# #     sys.stdout = output_capture= io.StringIO()
# #     try:
# #         exec(code)
# #         output = output_capture.getvalue()
# #         print('output:', output)
# #         return output
# #     except Exception as e:
# #         return str(e)
# #     finally:
# #         sys.stdout = original_stdout

# # def execute_java_code(code):
# #     try: 
# #         print('Executing Java code we have recieved...',code)
# #         with open('/tmp/Main.java', 'w') as java_file:
# #             java_file.write(code)
# #         compile_result = subprocess.run(['javac', '/tmp/Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# #         print('Compile result:', compile_result.returncode, compile_result.stdout, compile_result.stderr)
# #         if compile_result.returncode != 0:
# #             return compile_result.stderr.decode()
# #         run_result = subprocess.run(['java', '-classpath', '/tmp', 'Main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# #         print('Run result:', run_result.returncode, run_result.stdout, run_result.stderr)
# #         return run_result.stdout.decode() 
# #     except Exception as e:
# #         return str(e)
# # def execute_cpp_code(code):
# #     try:
# #         print('Executing C++ code we have recieved...',code)
# #         with open('/tmp/main.cpp', 'w') as cpp_file:
# #             cpp_file.write(code)
# #         compile_result = subprocess.run(['g++', '/tmp/main.cpp', '-o', '/tmp/main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# #         print('Compile result:', compile_result.returncode, compile_result.stdout, compile_result.stderr)
# #         if compile_result.returncode != 0:
# #             return compile_result.stderr.decode()
# #         run_result = subprocess.run(['/tmp/main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# #         print('Run result:', run_result.returncode, run_result.stdout, run_result.stderr)
# #         return run_result.stdout.decode() 
# #     except Exception as e:
# #         return str(e)

# # def handler(evenet,context):
# #     language = evenet.get('language', 'python')
# #     if language=='python':
# #         result=execute_python_code(code)
# #     elif language=='java':
# #         result=execute_java_code(code)
# #     elif language=='cpp':
# #         result=execute_cpp_code(code)
# #     # elif language=='javascript':
# #     #     result=execute_javascript_code(code)
# #     else:
# #         result='Unsupported language'
# #     return {
# #         'statusCode': 200,
# #         'body': result
# #     }
# #     return 'Hello Compiler' +sys.version+'!'


# import sys
# import subprocess
# import io
# import json

# def execute_python_code(code):
#     original_stdout = sys.stdout
#     sys.stdout = output_capture = io.StringIO()
#     try:
#         exec(code)
#         return output_capture.getvalue()
#     except Exception as e:
#         return str(e)
#     finally:
#         sys.stdout = original_stdout


# def execute_java_code(code):
#     try:
#         with open('/tmp/Main.java', 'w') as java_file:
#             java_file.write(code)

#         compile_result = subprocess.run(
#             ['javac', '/tmp/Main.java'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )

#         if compile_result.returncode != 0:
#             return compile_result.stderr.decode()

#         run_result = subprocess.run(
#             ['java', '-classpath', '/tmp', 'Main'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )

#         return run_result.stdout.decode()

#     except Exception as e:
#         return str(e)


# def execute_cpp_code(code):
#     try:
#         with open('/tmp/main.cpp', 'w') as cpp_file:
#             cpp_file.write(code)

#         compile_result = subprocess.run(
#             ['g++', '/tmp/main.cpp', '-o', '/tmp/main'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )

#         if compile_result.returncode != 0:
#             return compile_result.stderr.decode()

#         run_result = subprocess.run(
#             ['/tmp/main'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )

#         return run_result.stdout.decode()

#     except Exception as e:
#         return str(e)


# def handler(event, context):
#     # Parse input
#     body = event if isinstance(event, dict) else json.loads(event)

#     language = body.get('language', 'python')
#     code = body.get('code', '')

#     if language == 'python':
#         result = execute_python_code(code)
#     elif language == 'java':
#         result = execute_java_code(code)
#     elif language == 'cpp':
#         result = execute_cpp_code(code)
#     else:
#         result = 'Unsupported language'

#     return {
#         'statusCode': 200,
#         'body': result
#     }


import sys
import subprocess
import io
import json
import tempfile
import os
import shutil
import re
import traceback

# ------------------ PYTHON ------------------
def execute_python_code(code):
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = sys.stderr = output_capture = io.StringIO()
    try:
        # Use a single dictionary for globals and locals to solve function scoping issues
        execution_scope = {
            "__builtins__": __builtins__,
            "__name__": "__main__"
        }
        exec(code, execution_scope)
        return output_capture.getvalue()
    except Exception as e:
        # Clean up the traceback to remove internal stack frames from lambda_function
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_list = traceback.format_exception(exc_type, exc_value, exc_tb)
        cleaned_tb = []
        for line in tb_list:
            if "lambda_function.py" in line or "exec(code" in line:
                continue
            cleaned_tb.append(line)
        # Return stdout/stderr printed before the crash combined with the traceback
        return output_capture.getvalue() + "".join(cleaned_tb)
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr


# ------------------ JAVA ------------------
def execute_java_code(code):
    # Parse for public class name (Java requires filename to match public class)
    match = re.search(r'public\s+class\s+(\w+)', code)
    class_name = match.group(1) if match else 'Main'

    temp_dir = tempfile.mkdtemp()
    java_file_path = os.path.join(temp_dir, f"{class_name}.java")

    try:
        with open(java_file_path, 'w', encoding='utf-8') as java_file:
            java_file.write(code)

        # Compile the Java file
        compile_result = subprocess.run(
            ['javac', java_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if compile_result.returncode != 0:
            err_msg = compile_result.stderr.decode('utf-8', errors='replace')
            # Hide the full temporary directory path from user facing logs
            return err_msg.replace(temp_dir, "")

        # Run the compiled Java class
        run_result = subprocess.run(
            ['java', '-classpath', temp_dir, class_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if run_result.returncode != 0:
            return run_result.stderr.decode('utf-8', errors='replace').replace(temp_dir, "")

        return run_result.stdout.decode('utf-8', errors='replace')

    except subprocess.TimeoutExpired:
        return "Execution timed out (5 seconds limit exceeded)"
    except FileNotFoundError:
        return "Java compiler/runtime (javac/java) not found on the system. Please ensure they are installed and in the PATH."
    except Exception as e:
        return str(e)
    finally:
        # Cleanup temporary directory
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass


# ------------------ C++ ------------------
def execute_cpp_code(code):
    temp_dir = tempfile.mkdtemp()
    cpp_file_path = os.path.join(temp_dir, "main.cpp")
    exe_name = "main.exe" if os.name == 'nt' else "main"
    exe_path = os.path.join(temp_dir, exe_name)

    try:
        with open(cpp_file_path, 'w', encoding='utf-8') as cpp_file:
            cpp_file.write(code)

        # Compile C++ code
        compile_result = subprocess.run(
            ['g++', cpp_file_path, '-o', exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if compile_result.returncode != 0:
            err_msg = compile_result.stderr.decode('utf-8', errors='replace')
            return err_msg.replace(temp_dir, "")

        # Run binary
        run_result = subprocess.run(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if run_result.returncode != 0:
            return run_result.stderr.decode('utf-8', errors='replace').replace(temp_dir, "")

        return run_result.stdout.decode('utf-8', errors='replace')

    except subprocess.TimeoutExpired:
        return "Execution timed out (5 seconds limit exceeded)"
    except FileNotFoundError:
        return "C++ compiler (g++) not found on the system. Please ensure it is installed and in the PATH."
    except Exception as e:
        return str(e)
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass


# ------------------ C ------------------
def execute_c_code(code):
    temp_dir = tempfile.mkdtemp()
    c_file_path = os.path.join(temp_dir, "main.c")
    exe_name = "main.exe" if os.name == 'nt' else "main"
    exe_path = os.path.join(temp_dir, exe_name)

    try:
        with open(c_file_path, 'w', encoding='utf-8') as c_file:
            c_file.write(code)

        # Compile C code using gcc
        compile_result = subprocess.run(
            ['gcc', c_file_path, '-o', exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if compile_result.returncode != 0:
            err_msg = compile_result.stderr.decode('utf-8', errors='replace')
            return err_msg.replace(temp_dir, "")

        # Run binary
        run_result = subprocess.run(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if run_result.returncode != 0:
            return run_result.stderr.decode('utf-8', errors='replace').replace(temp_dir, "")

        return run_result.stdout.decode('utf-8', errors='replace')

    except subprocess.TimeoutExpired:
        return "Execution timed out (5 seconds limit exceeded)"
    except FileNotFoundError:
        return "C compiler (gcc) not found on the system. Please ensure it is installed and in the PATH."
    except Exception as e:
        return str(e)
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass


# ------------------ HANDLER ------------------
def handler(event, context):

    # ✅ Handle CORS preflight request
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": ""
        }

    try:
        # Parse request body safely
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        language = body.get("language", "python")
        code = body.get("code", "")

        if not code:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": "No code provided"
            }

        # Execute based on language
        if language == "python":
            result = execute_python_code(code)
        elif language == "java":
            result = execute_java_code(code)
        elif language == "cpp":
            result = execute_cpp_code(code)
        elif language == "c":
            result = execute_c_code(code)
        else:
            result = f"Unsupported language: {language}"

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": json.dumps({"output": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }