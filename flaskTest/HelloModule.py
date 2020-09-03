def func():
    print("function working")

# 이 모듈을 직접 실행하면 if 안에 구문이 실행된다.
if __name__ == '__main__':
    print("직접 실행")
    print(__name__)

else:
    print("임포트되어 실행")
    print(__name__)

