import sys
import os

# Add directory to sys.path so we can import lambda_function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lambda_function import execute_python_code, execute_java_code, execute_cpp_code, execute_c_code

def test_python_success():
    print("Testing python execution success...")
    code = "print('Hello ' + 'World')"
    res = execute_python_code(code)
    assert res.strip() == "Hello World", f"Expected 'Hello World', got '{res}'"
    print("[OK] Python execution success passed.")

def test_python_isolation():
    print("Testing python isolation...")
    # Attempt to write to a variable that might pollute the environment
    code1 = "my_custom_var = 123\nprint(my_custom_var)"
    res1 = execute_python_code(code1)
    assert res1.strip() == "123"
    
    # Run code2 which checks if my_custom_var leaked
    code2 = "try:\n    print(my_custom_var)\nexcept NameError:\n    print('isolated')"
    res2 = execute_python_code(code2)
    assert res2.strip() == "isolated", f"Expected 'isolated' due to namespace isolation, got '{res2}'"
    print("[OK] Python isolation passed.")

def test_python_scoping():
    print("Testing python scoping inside functions...")
    code = """
x = 42
def get_x():
    return x
print(get_x())
"""
    res = execute_python_code(code)
    assert res.strip() == "42", f"Expected '42', got '{res}'"
    print("[OK] Python function scoping passed.")

def test_python_error():
    print("Testing python traceback formatting...")
    code = "1 / 0"
    res = execute_python_code(code)
    assert "ZeroDivisionError" in res, f"Expected ZeroDivisionError traceback, got '{res}'"
    assert "lambda_function" not in res, "Traceback should be cleaned and not contain lambda_function internals"
    print("[OK] Python traceback formatting passed.")

def test_java_compilation():
    print("Testing Java execution with custom class name...")
    code = """
    public class CustomHello {
        public static void main(String[] args) {
            System.out.println("Java Custom Hello");
        }
    }
    """
    res = execute_java_code(code)
    if "Java compiler/runtime" in res:
        print("[WARN] Java compiler not installed on host. Skipping Java verification.")
    else:
        assert res.strip() == "Java Custom Hello", f"Expected 'Java Custom Hello', got '{res}'"
        print("[OK] Java execution with custom class name passed.")

def test_c_compilation():
    print("Testing C execution...")
    code = """
    #include <stdio.h>
    int main() {
        printf("C Success");
        return 0;
    }
    """
    res = execute_c_code(code)
    if "C compiler" in res:
        print("[WARN] C compiler (gcc) not installed on host. Skipping C verification.")
    else:
        assert res.strip() == "C Success", f"Expected 'C Success', got '{res}'"
        print("[OK] C execution passed.")

def test_cpp_compilation():
    print("Testing C++ execution...")
    code = """
    #include <iostream>
    int main() {
        std::cout << "CPP Success";
        return 0;
    }
    """
    res = execute_cpp_code(code)
    if "C++ compiler" in res:
        print("[WARN] C++ compiler (g++) not installed on host. Skipping C++ verification.")
    else:
        assert res.strip() == "CPP Success", f"Expected 'CPP Success', got '{res}'"
        print("[OK] C++ execution passed.")

if __name__ == "__main__":
    print("Running backend tests...")
    try:
        test_python_success()
        test_python_isolation()
        test_python_scoping()
        test_python_error()
        test_java_compilation()
        test_c_compilation()
        test_cpp_compilation()
        print("\nAll backend test functions completed successfully!")
    except AssertionError as e:
        print(f"\nTest verification failed: {e}")
        sys.exit(1)
