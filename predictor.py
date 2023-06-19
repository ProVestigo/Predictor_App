import random
import sys


class Predictor:
    def __init__(self):
        self.data_dict = dict()
        self.balance = 1000
        self.triad_list = []

    def input_filter(self):
        filtered = []
        data = input("\n")
        if data.lower() == "enough":
            print("Game over!")
            sys.exit()
        for i in data:
            if i == "0" or i == "1":
                filtered.append(i)
        return ''.join(filtered)

    def get_char_limit(self, limit=100):
        result = ''
        while len(result) < limit:
            print(f"The current data length is {len(result)}, "
                  f"{limit - len(result)} symbols left")
            print("Print a random string containing 0 or 1:")
            filtered = self.input_filter()
            result += filtered
        return result

    def generate_triads(self):
        for i in range(8):
            self.triad_list.append(bin(int(i))[2:].zfill(3))


    def create_data_dict(self):
        for triad in self.triad_list:
            self.data_dict[triad] = [0, 0]

    def create_prediction_data(self, data_string):
        for triad in self.triad_list:
            for i in range(len(data_string) - 3):
                if data_string[i:i + 3] == triad:
                    if data_string[i + 3] == "0":
                        self.data_dict[triad][0] += 1
                    else:
                        self.data_dict[triad][1] += 1

    def get_test_string(self, limit=4):
        test_string = ''
        while len(test_string) < limit:
            print("Print a random string containing 0 or 1:")
            test_string = self.input_filter()
        return test_string

    def generate_predictions(self):
        self.predictions = []
        test_string = self.get_test_string()
        for i in range(len(test_string) - 3):
            next_triad = test_string[i:i + 3]
            zeros, ones = self.data_dict[next_triad][0], self.data_dict[next_triad][1]
            if zeros > ones:
                self.predictions.append("0")
            elif zeros < ones:
                self.predictions.append("1")
            else:
                self.predictions.append(random.choice("01"))
        print(f"predictions:\n{''.join(self.predictions)}\n")
        correct, total, accuracy = self.calculate_accuracy(test_string)
        print(f"Computer guessed {correct} out of {total} symbols right ({accuracy} %)")
        wrong = total - correct
        self.balance += wrong
        self.balance -= correct
        print(f"Your balance is now ${self.balance}")
        return test_string

    def calculate_accuracy(self, test_string):
        correct = 0
        for i in range(len(test_string) - 3):
            if test_string[i + 3] == self.predictions[i]:
                correct += 1
        total = len(test_string) - 3
        accuracy = round(correct / total * 100, 2)
        return correct, total, accuracy

    def game_loop(self):
        print('You have $1000. Every time the system '
        'successfully predicts your next press, you lose $1.\n'
        'Otherwise, you earn $1. Print "enough" to leave '
        'the game. Let\'s go!\n')

        while True:
            new_data = self.generate_predictions()

            # Update prediction data with user input to increase accuracy
            self.create_prediction_data(new_data)


    def main(self):
        # Get initial dataset
        print("Please provide AI some data to learn...")
        data_string = self.get_char_limit()
        print(f"\nFinal data string:\n{data_string}\n\n")
        self.generate_triads()

        # Populate dict with all possible triads and prediction data
        self.create_data_dict()
        self.create_prediction_data(data_string)

        # Show prediction weights for each triad ("triad": zeros, ones)
        # for k, v in stats_dict.items():
        #     print(f"{k}: {v[0]},{v[1]}")

        # Continuously ask for data until user enters "enough"
        self.game_loop()


if __name__ == "__main__":
    P1 = Predictor()
    P1.main()
