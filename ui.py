from tkinter import *
from tkinter.filedialog import askopenfilename
from typing import Callable
from enum import Enum
from inspect import signature


def example_callback():
    print("yay it works")


def example_callback_param(p: str):
    print(f"yayyy {p}")

def example_callback_int(p: int):
    print(f"yayyy {p}")


class UiElement(Enum):
    SELECT_PATIENT = 0
    SELECT_CONTROL = 1
    SELECT_GRAPH = 2
    BUTTON_CALC = 3
    RADIO_PLOT = 4
    OUT_LGPS = 5
    OUT_RGPS = 6
    OUT_GPS = 7


class Ui:
    def add_select_callback(self, element: UiElement, *callbacks: Callable[[str], None]):
        for c in callbacks:
            match element:
                case UiElement.SELECT_PATIENT:
                    self.select_patient_callbacks.append(c)
                case UiElement.SELECT_CONTROL:
                    self.select_control_callbacks.append(c)
                case UiElement.SELECT_GRAPH:
                    self.select_graph_callbacks.append(c)
                case _:
                    raise TypeError(f"{element} is not a SELECT element")

    def add_button_callback(self, element: UiElement, *callbacks: Callable[[None], None]):
        for c in callbacks:
            match element:
                case UiElement.BUTTON_CALC:
                    self.button_calc_callbacks.append(c)
                case _:
                    raise TypeError(f"{element} is not a BUTTON element")

    def add_radio_callback(self, element: UiElement, *callbacks: Callable[[int], None]):
        for c in callbacks:
            match element:
                case UiElement.RADIO_PLOT:
                    self.button_calc_callbacks.append(c)
                case _:
                    raise TypeError(f"{element} is not a RADIO element")

    def get_value(self, element: UiElement) -> str|int|None:
        pass

    def set_element(self, element: UiElement, value: str):
        match element:
            case UiElement.OUT_LGPS:
                self.lgps_output.config(state=NORMAL)
                self.lgps_output.insert(END, value)
                self.lgps_output.config(state=DISABLED)
            case UiElement.OUT_RGPS:
                self.rgps_output.config(state=NORMAL)
                self.rgps_output.insert(END, value)
                self.rgps_output.config(state=DISABLED)
            case UiElement.OUT_GPS:
                self.gps_output.config(state=NORMAL)
                self.gps_output.insert(END, value)
                self.gps_output.config(state=DISABLED)
            case _:
                raise TypeError(f"{element} is not a OUT element")


    def _patient_select(self):
        f = askopenfilename()
        for c in self.select_patient_callbacks:
            c(f)

    def _control_select(self):
        f = askopenfilename()
        for c in self.select_control_callbacks:
            c(f)

    def mainloop(self):
        self.win.mainloop()

    def __init__(self):
        self.select_patient_callbacks: list[Callable[[str], None]] = []
        self.select_control_callbacks: list[Callable[[str], None]] = []
        self.button_calc_callbacks: list[Callable[[None], None]] = [example_callback, example_callback]
        self.select_graph_callbacks: list[Callable[[str], None]] = []
        self.radio_plot_callbacks: list[Callable[[int], None]] = [example_callback_int]

        self.add_select_callback(UiElement.SELECT_GRAPH, example_callback_param)
        self.add_select_callback(UiElement.SELECT_PATIENT, example_callback_param)

        self.win = Tk()
        self.win.title("GPS Calculator")

        root = Frame(self.win, padx=10, pady=10)
        root.pack()

        file_sel_frame = Frame(root, padx=10, pady=10)
        file_sel_frame.grid(row=0, column=0, sticky="W")

        self.patient_select = Button(file_sel_frame, text="Select patient", command=self._patient_select)
        self.patient_select.grid(row=0, sticky="W")
        self.control_select = Button(file_sel_frame, text="Select control", command=self._control_select)
        self.control_select.grid(row=1, sticky="W")

        gps_calc_frame = Frame(root, padx=10, pady=10)
        gps_calc_frame.grid(row=0, column=1, sticky="W")

        Button(gps_calc_frame,
               text="Calculate GPS",
               width=8,
               wraplength=60,
               command=lambda: [c() for c in self.button_calc_callbacks],
               ).grid(column=0, rowspan=3, sticky="W")
        Label(gps_calc_frame, text="LGPS", padx=10).grid(column=1, row=0)
        Label(gps_calc_frame, text="RGPS", padx=10).grid(column=1, row=1)
        Label(gps_calc_frame, text="GPS", padx=10).grid(column=1, row=2)

        self.lgps_output = Text(gps_calc_frame, height=1, width=4)
        self.lgps_output.insert(END, "10")
        self.lgps_output.config(state=DISABLED)
        self.lgps_output.grid(column=2, row=0)

        self.rgps_output = Text(gps_calc_frame, height=1, width=4)
        self.rgps_output.insert(END, "10")
        self.rgps_output.config(state=DISABLED)
        self.rgps_output.grid(column=2, row=1)

        self.gps_output = Text(gps_calc_frame, height=1, width=4)
        self.gps_output.insert(END, "10")
        self.gps_output.config(state=DISABLED)
        self.gps_output.grid(column=2, row=2)

        graph_control_frame = Frame(root, padx=10, pady=10)
        graph_control_frame.grid(row=1, column=0, sticky="W")

        self.select_graph = StringVar(graph_control_frame, "Select")
        graph_dropdown = OptionMenu(graph_control_frame,
                                    self.select_graph,
                                    "option",
                                    "other option",
                                    "other other option",
                                    command=lambda x: [c(x) for c in self.select_graph_callbacks])
        graph_dropdown.grid(column=0, row=0, sticky="W")

        graph_radio_frame = Frame(root)
        graph_radio_frame.grid(row=1, column=1, sticky="W")
        self.graph_radio = IntVar()

        Radiobutton(graph_radio_frame,
                    text="Show graphs",
                    value=1,
                    variable=self.graph_radio,
                    anchor="e",
                    command=lambda: [c(self.graph_radio.get()) for c in self.radio_plot_callbacks]
                    ).pack(anchor="w")
        Radiobutton(graph_radio_frame,
                    text="Show GPS",
                    value=2,
                    variable=self.graph_radio,
                    anchor="e",
                    command=lambda: [c(self.graph_radio.get()) for c in self.radio_plot_callbacks]
                    ).pack(anchor="w")

        graph_frame = Frame(root, width=400, height=300, padx=10, pady=10, background="black")
        graph_frame.grid(row=2, columnspan=2)