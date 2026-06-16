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


# ------------------ PYTHON ------------------
def execute_python_code(code):
    original_stdout = sys.stdout
    sys.stdout = output_capture = io.StringIO()
    try:
        exec(code)
        return output_capture.getvalue()
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = original_stdout


# ------------------ JAVA ------------------
def execute_java_code(code):
    try:
        with open('/tmp/Main.java', 'w') as java_file:
            java_file.write(code)

        compile_result = subprocess.run(
            ['javac', '/tmp/Main.java'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if compile_result.returncode != 0:
            return compile_result.stderr.decode()

        run_result = subprocess.run(
            ['java', '-classpath', '/tmp', 'Main'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        return run_result.stdout.decode()

    except subprocess.TimeoutExpired:
        return "Execution timed out"
    except Exception as e:
        return str(e)


# ------------------ C++ ------------------
def execute_cpp_code(code):
    try:
        with open('/tmp/main.cpp', 'w') as cpp_file:
            cpp_file.write(code)

        compile_result = subprocess.run(
            ['g++', '/tmp/main.cpp', '-o', '/tmp/main'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if compile_result.returncode != 0:
            return compile_result.stderr.decode()

        run_result = subprocess.run(
            ['/tmp/main'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        return run_result.stdout.decode()

    except subprocess.TimeoutExpired:
        return "Execution timed out"
    except Exception as e:
        return str(e)


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
        else:
            result = "Unsupported language"

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