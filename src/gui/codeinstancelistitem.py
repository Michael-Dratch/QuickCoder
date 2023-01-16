from functools import partial

from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel

from src.datastructures import Sentiment


class CodeInstanceListItem(QWidget):
    def __init__(self, codeInstance, showSentimentOptions):
        super().__init__()
        self.codeInstance = codeInstance
        self.showSentimentOptions = showSentimentOptions
        cutoff = 30
        text = codeInstance.text[:cutoff]
        if len(codeInstance.text) > cutoff:
            text += '...'

        self.sentimentButton = QPushButton()
        self.setButtonStyle(codeInstance, self.sentimentButton)
        self.sentimentButton.setToolTip('Change Sentiment')
        self.sentimentButton.clicked.connect(partial(self.showSentimentOptions, self.codeInstance, self))

        item_layout = QHBoxLayout()
        item_layout.addWidget(self.sentimentButton)
        item_layout.addWidget(QLabel(text))
        self.setLayout(item_layout)

    def setButtonStyle(self, instance, sentimentButton):
        if instance.sentiment:
            sentimentButton.setObjectName(instance.sentiment.name)
        else:
            sentimentButton.setObjectName('No-Sentiment')
        if instance.sentiment == Sentiment.POSITIVE:
            id = 'POSITIVE'
            color = 'green'
            hoverColor = 'darkgreen'
        elif instance.sentiment == Sentiment.NEGATIVE:
            id = 'NEGATIVE'
            color = 'red'
            hoverColor = 'darkred'
        elif instance.sentiment == Sentiment.NEUTRAL:
            id = 'NEUTRAL'
            color = '#f5c542'
            hoverColor = '#b38f2e'
        else:
            id = 'No-Sentiment'
            color = 'darkgrey'
            hoverColor = 'grey'

        sentimentButton.setStyleSheet(
            """QPushButton#{id} {{
                    background-color: {color};
                    max-width: 25px}}

            QPushButton#{id}:hover {{
                background-color: {hoverColor};
                max-width: 25px}}""".format(id=id, color=color, hoverColor=hoverColor))

    def updateSentimentButton(self):
        self.setButtonStyle(self.codeInstance, self.sentimentButton)

