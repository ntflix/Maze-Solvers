from modules.ui_processing_link_layer.ui_processing_link_layer import (
    UIProcessingLinkLayer,
)

if __name__ == "__main__":
    import logging

    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LEVEL = logging.ERROR
    logging.basicConfig(format=FORMAT, level=LEVEL)
    log = logging.getLogger()

    app = UIProcessingLinkLayer()
    app.start()
