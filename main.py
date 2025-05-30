import random
import tkinter as tk
from tkinter import ttk


class MatrixTrainer:
    def __init__(self, master):
        self.master = master
        master.title("Matrix Trainer")
        master.configure(bg="#f0f0f0")

        # Add a new instance variable for highlight mode
        self.highlight_mode = tk.BooleanVar(value=True)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Color scheme
        self.colors = {
            "primary": "#2563eb",
            "secondary": "#64748b",
            "success": "#059669",
            "warning": "#d97706",
            "background": "#f8fafc",
            "surface": "#ffffff",
            "text": "#1f2937",
            "border": "#e2e8f0",
        }

        self.configure_styles()

        self.max_dim = 4
        self.zoom_factor = 1.0

        # Main container with padding
        self.main_container = tk.Frame(
            master, bg=self.colors["background"], padx=20, pady=20
        )
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = tk.Label(
            self.main_container,
            text="Matrix Multiplication Trainer",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"],
        )
        self.title_label.pack(pady=(0, 20))

        # Matrix container with better styling
        self.mat_frame = tk.Frame(self.main_container, bg=self.colors["background"])
        self.mat_frame.pack(pady=20)

        self.create_matrix_frames()

        # Control panel with better styling
        self.control_panel = tk.Frame(self.main_container, bg=self.colors["background"])
        self.control_panel.pack(pady=20)

        self.create_control_buttons()

        self.hidden_indices = []
        self.revealed = -1

        # Bind hotkeys
        self.master.bind("<Right>", lambda e: self.reveal_next())
        self.master.bind("<Left>", lambda e: self.reveal_prev())
        self.master.bind("<space>", lambda e: self.generate())
        self.master.bind("<Return>", lambda e: self.reveal_all())

    def configure_styles(self):
        """Configure custom styles for ttk widgets."""
        # Button styles
        self.style.configure(
            "Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8)
        )

        self.style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=(8, 6))

        self.style.configure(
            "Zoom.TButton", font=("Segoe UI", 12, "bold"), padding=(8, 8)
        )

        # Checkbox style
        self.style.configure("TCheckbutton", font=("Segoe UI", 10))

    def create_matrix_frames(self):
        """Create styled matrix frames."""
        # Frame A
        self.frame_A = tk.LabelFrame(
            self.mat_frame,
            text="Matrix A",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["surface"],
            relief="solid",
            borderwidth=2,
            padx=15,
            pady=15,
        )
        self.frame_A.grid(row=0, column=0, padx=15, pady=10)

        # Frame B
        self.frame_B = tk.LabelFrame(
            self.mat_frame,
            text="Matrix B",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["surface"],
            relief="solid",
            borderwidth=2,
            padx=15,
            pady=15,
        )
        self.frame_B.grid(row=0, column=1, padx=15, pady=10)

        # Multiplication symbol
        self.mult_label = tk.Label(
            self.mat_frame,
            text="×",
            font=("Segoe UI", 24, "bold"),
            fg=self.colors["warning"],
            bg=self.colors["background"],
        )
        self.mult_label.grid(row=0, column=2, padx=10)

        # Frame C
        self.frame_C = tk.LabelFrame(
            self.mat_frame,
            text="Result: C = A × B",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors["success"],
            bg=self.colors["surface"],
            relief="solid",
            borderwidth=2,
            padx=15,
            pady=15,
        )
        self.frame_C.grid(row=0, column=3, padx=15, pady=10)

    def create_highlight_checkbox(self):
        """Create a checkbox for highlighting numbers to be multiplied."""
        self.highlight_checkbox = ttk.Checkbutton(
            self.control_panel,
            text="Highlight Numbers to Multiply",
            variable=self.highlight_mode,
            style="TCheckbutton",
            command=self.update_c_display,
        )
        self.highlight_checkbox.pack(side=tk.LEFT, padx=10)

    def create_control_buttons(self):
        """Create styled control buttons."""
        # Zoom controls
        zoom_frame = tk.Frame(self.control_panel, bg=self.colors["background"])
        zoom_frame.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(
            zoom_frame,
            text="Zoom:",
            font=("Segoe UI", 10),
            fg=self.colors["text"],
            bg=self.colors["background"],
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.zoom_out_btn = ttk.Button(
            zoom_frame, text="−", style="Zoom.TButton", command=self.zoom_out, width=3
        )
        self.zoom_out_btn.pack(side=tk.LEFT, padx=2)

        self.zoom_in_btn = ttk.Button(
            zoom_frame, text="+", style="Zoom.TButton", command=self.zoom_in, width=3
        )
        self.zoom_in_btn.pack(side=tk.LEFT, padx=2)

        # Main action buttons
        action_frame = tk.Frame(self.control_panel, bg=self.colors["background"])
        action_frame.pack(side=tk.LEFT, padx=10)

        self.gen_btn = ttk.Button(
            action_frame,
            text="Generate Random",
            style="Primary.TButton",
            command=self.generate,
        )
        self.gen_btn.pack(side=tk.LEFT, padx=5)

        self.full_btn = ttk.Button(
            action_frame,
            text="Show Solution",
            style="Secondary.TButton",
            command=self.reveal_all,
            state=tk.DISABLED,
        )
        self.full_btn.pack(side=tk.LEFT, padx=5)

        # Navigation buttons
        nav_frame = tk.Frame(self.control_panel, bg=self.colors["background"])
        nav_frame.pack(side=tk.LEFT, padx=(20, 0))

        self.prev_btn = ttk.Button(
            nav_frame,
            text="← Previous",
            style="Secondary.TButton",
            command=self.reveal_prev,
            state=tk.DISABLED,
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(
            nav_frame,
            text="Next →",
            style="Secondary.TButton",
            command=self.reveal_next,
            state=tk.DISABLED,
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Add highlight checkbox
        self.create_highlight_checkbox()

    def generate_random_matrix(self, rows, cols):
        return [[random.randint(-9, 9) for _ in range(cols)] for _ in range(rows)]

    def display_matrix(
        self,
        frame,
        matrix,
        matrix_type="normal",
        highlight_row=None,
        highlight_col=None,
        highlight_element=None,
    ):
        """Display a matrix with beautiful styling and optional highlighting."""
        for widget in frame.winfo_children():
            widget.destroy()

        font_size = int(12 * self.zoom_factor)
        width = max(4, int(4 * self.zoom_factor))
        height = max(2, int(2 * self.zoom_factor))

        # Color scheme based on matrix type
        if matrix_type == "result":
            bg_color = "#fef3c7"  # Light yellow for results
            text_color = self.colors["text"]
        elif matrix_type == "unknown":
            bg_color = "#fee2e2"  # Light red for unknowns
            text_color = "#991b1b"
        else:
            bg_color = self.colors["surface"]
            text_color = self.colors["text"]

        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                cell_bg = bg_color
                cell_text = text_color

                # Apply highlighting for factors being multiplied
                if highlight_row is not None and i == highlight_row:
                    cell_bg = "#dbeafe"  # Light blue for highlighted row
                    cell_text = "#1e40af"  # Dark blue text
                elif highlight_col is not None and j == highlight_col:
                    cell_bg = "#dbeafe"  # Light blue for highlighted column
                    cell_text = "#1e40af"  # Dark blue text

                if str(val) == "?":
                    cell_bg = "#fee2e2"
                    cell_text = "#991b1b"

                if highlight_element is not None and (i, j) == highlight_element:
                    cell_bg = "#dbeafe"  # Light blue for highlighted element
                    cell_text = "#1e40af"  # Dark blue text

                lbl = tk.Label(
                    frame,
                    text=str(val),
                    width=width,
                    height=height,
                    borderwidth=1,
                    relief="solid",
                    font=(
                        "Segoe UI",
                        font_size,
                        "bold" if str(val) != "?" else "normal",
                    ),
                    bg=cell_bg,
                    fg=cell_text,
                    bd=1,
                )
                lbl.grid(row=i, column=j, padx=2, pady=2)

    def zoom_in(self):
        if self.zoom_factor < 3.0:
            self.zoom_factor += 0.1
            self.refresh_zoom()

    def zoom_out(self):
        if self.zoom_factor > 0.5:
            self.zoom_factor -= 0.1
            self.refresh_zoom()

    def refresh_zoom(self):
        if hasattr(self, "A") and hasattr(self, "B"):
            # Determine current highlighting
            highlight_row_a = None
            highlight_col_b = None
            highlight_element_a = None
            highlight_element_b = None

            if (
                hasattr(self, "multiplication_steps")
                and self.current_step >= 0
                and self.current_step < len(self.multiplication_steps)
            ):
                current_i, current_j, current_k = self.multiplication_steps[
                    self.current_step
                ]

                if self.highlight_mode.get():
                    # Checkbox checked: highlight only specific elements
                    highlight_element_a = (current_i, current_k)
                    highlight_element_b = (current_k, current_j)
                else:
                    # Checkbox unchecked: highlight entire row/column
                    highlight_row_a = current_i
                    highlight_col_b = current_j

            self.display_matrix(
                self.frame_A,
                self.A,
                highlight_row=highlight_row_a,
                highlight_element=highlight_element_a,
            )
            self.display_matrix(
                self.frame_B,
                self.B,
                highlight_col=highlight_col_b,
                highlight_element=highlight_element_b,
            )
        if hasattr(self, "C"):
            self.update_c_display()

    def generate(self):
        """Generate new random matrices with visual feedback."""
        n = random.choices([1, 2, 3, 4], weights=[0.1, 0.2, 0.3, 0.4])[0]
        m = random.choices([1, 2, 3, 4], weights=[0.1, 0.2, 0.3, 0.4])[0]
        p = random.choices([1, 2, 3, 4], weights=[0.1, 0.2, 0.3, 0.4])[0]

        self.A = self.generate_random_matrix(n, m)
        self.B = self.generate_random_matrix(m, p)
        self.C = [
            [sum(self.A[i][k] * self.B[k][j] for k in range(m)) for j in range(p)]
            for i in range(n)
        ]

        self.display_matrix(self.frame_A, self.A)
        self.display_matrix(self.frame_B, self.B)
        self.display_matrix(
            self.frame_C, [["?" for _ in range(p)] for _ in range(n)], "unknown"
        )

        # Create steps for each individual multiplication
        self.multiplication_steps = []
        for i in range(n):
            for j in range(p):
                for k in range(m):
                    self.multiplication_steps.append((i, j, k))

        self.current_step = -1
        self.completed_results = set()  # Track which C[i][j] are complete

        # Update button states
        self.next_btn.config(state=tk.NORMAL)
        self.prev_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.NORMAL)

    def update_c_display(self):
        """Update the display of matrix C with proper styling."""
        # Guard clause: return early if matrices haven't been generated yet
        if not hasattr(self, "C") or not hasattr(self, "multiplication_steps"):
            return

        p = len(self.C[0])
        n = len(self.C)
        m = len(self.A[0])
        disp = [["?" for _ in range(p)] for _ in range(n)]

        # Show completed results
        for i, j in self.completed_results:
            disp[i][j] = str(self.C[i][j])

        # Determine current highlighting
        highlight_row_a = None
        highlight_col_b = None
        highlight_element_a = None
        highlight_element_b = None

        if self.current_step >= 0 and self.current_step < len(
            self.multiplication_steps
        ):
            current_i, current_j, current_k = self.multiplication_steps[
                self.current_step
            ]

            if self.highlight_mode.get():
                # Checkbox checked: highlight only specific elements
                highlight_element_a = (current_i, current_k)
                highlight_element_b = (current_k, current_j)
            else:
                # Checkbox unchecked: highlight entire row/column
                highlight_row_a = current_i
                highlight_col_b = current_j

        # Check if we should reveal any new results based on completed multiplications
        # Only reveal results for cells where ALL multiplications have been shown AND we've moved past them
        if self.current_step >= 0:
            for i in range(n):
                for j in range(p):
                    if (i, j) not in self.completed_results:
                        # Find the last multiplication step for this cell
                        last_step_for_cell = -1
                        for idx, (step_i, step_j, step_k) in enumerate(
                            self.multiplication_steps
                        ):
                            if step_i == i and step_j == j:
                                last_step_for_cell = max(last_step_for_cell, idx)

                        # Only reveal result if we've moved PAST the last multiplication for this cell
                        # OR if we're at the very end (past all multiplication steps)
                        if (
                            last_step_for_cell >= 0
                            and self.current_step > last_step_for_cell
                        ) or (self.current_step >= len(self.multiplication_steps)):
                            self.completed_results.add((i, j))
                            disp[i][j] = str(self.C[i][j])

        # Update all matrix displays
        self.display_matrix(
            self.frame_A,
            self.A,
            highlight_row=highlight_row_a,
            highlight_element=highlight_element_a,
        )
        self.display_matrix(
            self.frame_B,
            self.B,
            highlight_col=highlight_col_b,
            highlight_element=highlight_element_b,
        )
        self.display_matrix(self.frame_C, disp, "result")

        # Update button states
        self.next_btn.config(
            state=tk.DISABLED
            if self.current_step >= len(self.multiplication_steps)
            else tk.NORMAL
        )
        self.prev_btn.config(state=tk.NORMAL if self.current_step >= 0 else tk.DISABLED)

    def reveal_next(self):
        if self.current_step + 1 < len(self.multiplication_steps):
            self.current_step += 1
            self.update_c_display()
        elif self.current_step + 1 == len(self.multiplication_steps):
            # We're at the end, move to a "final" state to reveal last results
            self.current_step += 1
            self.update_c_display()

    def reveal_prev(self):
        if self.current_step >= 0:
            self.current_step -= 1
            # Remove completed results that come after current step
            if hasattr(self, "multiplication_steps") and self.current_step >= 0:
                current_i, current_j, _ = self.multiplication_steps[self.current_step]
                # Remove any completed results that come after current position
                self.completed_results = {
                    (i, j)
                    for (i, j) in self.completed_results
                    if i < current_i or (i == current_i and j <= current_j)
                }
            else:
                self.completed_results.clear()
            self.update_c_display()

    def reveal_all(self):
        if hasattr(self, "multiplication_steps"):
            self.current_step = len(self.multiplication_steps) - 1
            # Add all result cells to completed
            n = len(self.C)
            p = len(self.C[0])
            self.completed_results = {(i, j) for i in range(n) for j in range(p)}
            self.update_c_display()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    root.resizable(True, True)
    app = MatrixTrainer(root)
    root.mainloop()
