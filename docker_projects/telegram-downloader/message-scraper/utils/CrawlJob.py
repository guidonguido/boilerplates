class CrawlJob:
    def __init__(
            self, 
            text, 
            packageName = None,
            comment = "",
            autoConfirm = "TRUE",
            autoStart = "TRUE",
            extractAfterDownload = "TRUE",
            forcedStart = "TRUE",
            overwritePackagizerEnabled = False):
        self.text = text
        self.packageName = packageName
        self.comment = comment
        self.autoConfirm = autoConfirm
        self.autoStart = autoStart
        self.extractAfterDownload = extractAfterDownload
        self.forcedStart = forcedStart
        self.overwritePackagizerEnabled = overwritePackagizerEnabled