# This Python script creates a GUI calculator with advanced operations using tkinter.

import tkinter as tk
from tkinter import messagebox # Used for displaying pop-up messages
import math # Import the math module for advanced operations like sqrt

class CalculatorApp:
  """
  A class to represent the Calculator application with a GUI.
  Handles the creation of the GUI, button clicks, and calculation logic.
  """
  def __init__(self, master):
    """
    Initializes the CalculatorApp.

    Args:
      master: The root Tkinter window.
    """
    self.master = master
    master.title("Advanced Calculator")
    master.geometry("320x480") # Increased window size to accommodate more buttons
    master.resizable(False, False) # Prevent resizing for simplicity
    master.configure(bg="#2c3e50") # Dark background for the window

    self.expression = "" # Stores the current expression as a string
    self.input_text = tk.StringVar() # Tkinter variable to update the display

    # Create the display entry widget
    self.input_frame = tk.Frame(master, bd=0, relief=tk.RIDGE, bg="#34495e")
    self.input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    self.input_field = tk.Entry(
        self.input_frame,
        font=('Arial', 28, 'bold'), # Slightly larger font for display
        textvariable=self.input_text,
        width=18,
        bg="#ecf0f1", # Light background for display
        fg="#2c3e50", # Dark text for display
        bd=0,
        justify=tk.RIGHT # Align text to the right
    )
    self.input_field.grid(row=0, column=0, ipadx=8, ipady=8, padx=5, pady=5, sticky="nsew")
    self.input_frame.grid_columnconfigure(0, weight=1) # Allow column to expand

    # Create the buttons frame
    self.buttons_frame = tk.Frame(master, bg="#2c3e50")
    self.buttons_frame.pack(fill=tk.BOTH, expand=True)

    # Define button layout and values
    # Each list represents a row of buttons.
    # Note: 'DEL' for backspace, '√' for square root, '^' for power
    button_texts = [
        ('C', 'DEL', '(', ')'),
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('√', '^', '.', '+'), # New row for advanced ops and common symbols
        ('0', '=', ' ') # ' ' is a placeholder for the grid
    ]

    # Configure grid weights for buttons_frame to make buttons expand
    for i in range(len(button_texts)): # Number of rows
        self.buttons_frame.grid_rowconfigure(i, weight=1)
    for i in range(4): # Number of columns
        self.buttons_frame.grid_columnconfigure(i, weight=1)

    # Create and place buttons
    for r_idx, row_buttons in enumerate(button_texts):
      for c_idx, button_text in enumerate(row_buttons):
        # Determine button command and special styling
        if button_text == '=':
          button = tk.Button(
              self.buttons_frame,
              text=button_text,
              font=('Arial', 20, 'bold'),
              command=self.calculate,
              bg="#27ae60", fg="white", activebackground="#2ecc71", bd=1, relief=tk.FLAT,
              highlightbackground="#2c3e50"
          )
          # Make the '=' button span two columns
          button.grid(row=r_idx, column=c_idx, columnspan=3, sticky="nsew", padx=2, pady=2)
        elif button_text == 'C':
          button = tk.Button(
              self.buttons_frame,
              text=button_text,
              font=('Arial', 20, 'bold'),
              command=self.clear_expression,
              bg="#e74c3c", fg="white", activebackground="#c0392b", bd=1, relief=tk.FLAT,
              highlightbackground="#2c3e50"
          )
          button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=2, pady=2)
        elif button_text == 'DEL':
          button = tk.Button(
              self.buttons_frame,
              text=button_text,
              font=('Arial', 20, 'bold'),
              command=self.delete_last_char,
              bg="#f1c40f", fg="#2c3e50", activebackground="#e6b911", bd=1, relief=tk.FLAT,
              highlightbackground="#2c3e50"
          )
          button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=2, pady=2)
        elif button_text in ('/', '*', '-', '+'):
          button = tk.Button(
              self.buttons_frame,
              text=button_text,
              font=('Arial', 20, 'bold'),
              command=lambda b=button_text: self.button_click(b),
              bg="#f39c12", fg="white", activebackground="#e67e22", bd=1, relief=tk.FLAT,
              highlightbackground="#2c3e50"
          )
          button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=2, pady=2)
        elif button_text == '√': # Square Root
          button = tk.Button(
              self.buttons_frame,
              text=button_text,
              font=('Arial', 20, 'bold'),
              command=lambda: self.button_click("math.sqrt("), # Appends 'math.sqrt('
              bg="#8e44ad", fg="white", activebackground="#9b59b6", bd=1, relief=tk.FLAT,
              highlightbackground="#2c3e50"
          )
          button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=2, pady=2)
        elif button_text == '^': # Power
          button = tk.Button(
              self.buttons_frame,
              text=button_text,
              font=('Arial', 20, 'bold'),
              command=lambda: self.button_click("**"), # Appends '**' for power
              bg="#8e44ad", fg="white", activebackground="#9b59b6", bd=1, relief=tk.FLAT,
              highlightbackground="#2c3e50"
          )
          button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=2, pady=2)
        elif button_text == ' ': # Empty placeholder cell
          # Skip creating a button for the placeholder
          continue
        else: # Numbers and parentheses
          button = tk.Button(
              self.buttons_frame,
              text=button_text,
              font=('Arial', 20, 'bold'),
              command=lambda b=button_text: self.button_click(b),
              bg="#3498db", fg="white", activebackground="#2980b9", bd=1, relief=tk.FLAT,
              highlightbackground="#2c3e50"
          )
          button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=2, pady=2)


  def button_click(self, char):
    """
    Appends the clicked character (number, operator, or function start)
    to the expression and updates the display.

    Args:
      char: The character string from the clicked button.
    """
    self.expression += str(char)
    self.input_text.set(self.expression) # Update the display

  def clear_expression(self):
    """Clears the entire current expression and the display."""
    self.expression = ""
    self.input_text.set("") # Clear the display

  def delete_last_char(self):
    """Removes the last character from the expression and updates the display (backspace)."""
    self.expression = self.expression[:-1] # Slices the string to remove the last char
    self.input_text.set(self.expression) # Update the display

  def calculate(self):
    """
    Evaluates the current expression and displays the result.
    Handles potential errors during evaluation.
    """
    try:
      # Evaluate the expression using eval().
      # We provide the 'math' module in the globals dictionary
      # so that math functions like sqrt() can be recognized.
      result = str(eval(self.expression, {"math": math}))
      self.input_text.set(result) # Display the result
      self.expression = result # Set expression to result for chained operations
    except ZeroDivisionError:
      messagebox.showerror("Error", "Cannot divide by zero!")
      self.clear_expression()
    except SyntaxError:
      messagebox.showerror("Error", "Invalid Expression! Check parentheses or operators.")
      self.clear_expression()
    except TypeError: # Catches errors like math.sqrt() on negative numbers or non-numbers
      messagebox.showerror("Error", "Invalid operation! Check inputs for functions like sqrt.")
      self.clear_expression()
    except Exception as e: # Catch any other unexpected errors
      messagebox.showerror("Error", f"An unexpected error occurred: {e}")
      self.clear_expression()

# Main entry point of the application
if __name__ == "__main__":
  root = tk.Tk() # Create the main window
  app = CalculatorApp(root) # Create an instance of the calculator app
  root.mainloop() # Start the Tkinter event loop, which keeps the window open
