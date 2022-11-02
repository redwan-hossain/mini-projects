from typing import Union


class ExhibitionGallery:
    __hall_list: list = []

    @classmethod
    def entry_hall(cls, new_hall) -> None:
        cls.__hall_list.append(new_hall)


class Hall(ExhibitionGallery):
    __track_show_id: list = []

    def __init__(self, rows: int, cols: int, hall_no: str) -> None:
        self.__hall_no = hall_no
        self.__rows = rows
        self.__cols = cols
        self.__seats: dict = {}
        self.__show_list: list[tuple] = []
        super().entry_hall(new_hall=(self.__rows, self.__cols, self.__hall_no))

    def get_hall_no(self) -> str:
        return self.__hall_no

    def get_exhibition_info_by_id(self, exhibition_id: str) -> None:
        if exhibition_id == self.__show_list[0][0]:
            print("Exhibition name:", self.__show_list[0][1], end="\t\t")
            print("Exhibition Time:", self.__show_list[0][2])
        elif exhibition_id == self.__show_list[1][0]:
            print("Exhibition name:", self.__show_list[1][1], end="\t\t")
            print("Exhibition Time:", self.__show_list[1][2])

    def entry_show(self, show_id: str, exhibition_name: str, time: str) -> None:
        self.__show_list.append((show_id, exhibition_name, time))
        Hall.__track_show_id.append(show_id)
        __seat_plan: list = [
            [False for d in range(int(self.__cols))] for f in range(int(self.__rows))
        ]
        self.__seats[f"{show_id}"] = __seat_plan

    def view_show_list(self) -> None:
        print("\n")
        print("Available Shows:")
        print("-" * 50)
        print("ID\t\t Name\t\t\t Time")
        print("-" * 50)
        for exhibition in self.__show_list:
            print(f"{exhibition[0]}\t\t {exhibition[1]}\t\t {exhibition[2]}")
        print("\n")

    @staticmethod
    def validate_exhibition_id(exhibition_id: str) -> str:
        while True:
            if exhibition_id not in Hall.__track_show_id:
                print("Invalid Show ID")
                exhibition_id = input("Enter Again: ")
            else:
                break
        return exhibition_id

    def extract_seat_status(self, exhibition_id: str):
        get_data = self.__seats.get(f"{exhibition_id}")
        return get_data

    def view_available_seats(self, exhibition_id: str) -> None:
        key: str = Hall.validate_exhibition_id(exhibition_id)
        value: list = self.extract_seat_status(key)
        self.get_exhibition_info_by_id(key)
        print("Available seats (X means Unavailable seats):")
        print("-" * 25)
        for xyz, nested_list in enumerate(value):
            counter = -1
            for data in nested_list:
                counter += 1
                if not data:
                    print(f"{chr(xyz + 65)}{counter}\t\t", end="")
                else:
                    print("X\t\t", end="")
            print("\n", end="")
        print("-" * 25)

    def validate_seat_booking(
        self, exhibition_id: str, seat_no: str
    ) -> Union[str, int, bool]:
        key = Hall.validate_exhibition_id(exhibition_id)
        value = self.extract_seat_status(key)
        already_booked: list = []

        for xyz, nested_list in enumerate(value):
            counter = -1
            for data in nested_list:
                counter += 1
                translated_seat_no = f"{chr(xyz + 65)}{counter}"
                if not data:
                    if seat_no == translated_seat_no:
                        return seat_no
                else:
                    already_booked.append(translated_seat_no)
        for booked in already_booked:
            if seat_no == booked:
                return -1
        return False

    def book_seats(
        self, customer_name: str, phone_no: str, exhibition_id: str, seat_info: tuple
    ) -> str:
        key = Hall.validate_exhibition_id(exhibition_id)
        value = self.extract_seat_status(key)

        for seat in seat_info:
            first = str(seat[0])
            second = int(seat[1])
            first_converted = int(ord(first) - 65)
            value[first_converted][second] = True
        return f"ticket/s booked for {customer_name} with phone no {phone_no}"


if __name__ == "__main__":
    hall_01 = Hall(4, 3, "ZE-13")
    hall_01.entry_show("his", "Historical", "23-10-2022 (10 AM)")
    hall_01.entry_show("lit", "Literature", "25-10-2022 (12 PM)")
    while True:
        print("1. Running show list")
        print("2. View available seats")
        print("3. Book ticket")
        print("0. Exit")

        choice = input("Enter your choice: ")
        if choice.lower() == "0":
            break

        elif choice.lower() == "1":
            hall_01.view_show_list()

        elif choice.lower() == "2":
            show_id_input = input("Enter Show Id: ")
            hall_01.view_available_seats(f"{show_id_input}")

        elif choice.lower() == "3":
            buyer_name = input("Enter your name: ")
            buyer_phone_no = input("Enter your phone number: ")
            ticket_freq = int(input("How many seats do you want to book? "))
            show_id_input = input("Enter Show Id: ")
            verify_exhibition_id_input = hall_01.validate_exhibition_id(show_id_input)
            total_booked_seat: list = []

            for i in range(ticket_freq):
                while True:
                    seat_no_input = input("Enter Seat No:")
                    capture = hall_01.validate_seat_booking(
                        verify_exhibition_id_input, seat_no_input
                    )
                    if capture == -1:
                        print(f"{seat_no_input} is already booked.")
                    elif capture:
                        total_booked_seat.append(capture)
                        break
                    else:
                        print("Invalid seat number ->", seat_no_input)
            seat_tuple = tuple(total_booked_seat)
            confirmation_msg = hall_01.book_seats(
                buyer_name, buyer_phone_no, verify_exhibition_id_input, seat_tuple
            )

            print(f"{ticket_freq}", confirmation_msg)
            hall_01.get_exhibition_info_by_id(f"{verify_exhibition_id_input}")
            print("Hall ID:", hall_01.get_hall_no())
            print("Booked seat number/s: :", end=" ")
            for label in seat_tuple:
                print(label, end=" ")
            print("\n")
