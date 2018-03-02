# Copy of ListTrainer with progress bar removed

from chatterbot.conversation import Response
from chatterbot.trainers import Trainer

class CustomListTrainer(Trainer):
    """
    Allows a chat bot to be trained using a list of strings
    where the list represents a conversation.
    """

    def train(self, conversation):
        """
        Train the chat bot based on the provided list of
        statements that represents a single conversation.
        """
        previous_statement_text = None

        for conversation_count, text in enumerate(conversation):
            
            #print_progress_bar("List Trainer", conversation_count + 1, len(conversation))
            #print(1, end='')
            statement = self.get_or_create(text)

            if previous_statement_text:
                statement.add_response(
                    Response(previous_statement_text)
                )

            previous_statement_text = statement.text
            self.storage.update(statement)
