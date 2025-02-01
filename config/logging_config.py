import logging

# ✅ 로거 설정을 위한 함수
def get_logger(name="dummy_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # 상위 로거로 전파 방지
    logger.handlers.clear()  # 기존 핸들러 제거 (중복 방지)

    # ✅ 콘솔 핸들러 추가
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
