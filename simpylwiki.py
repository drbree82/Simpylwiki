import os  # Importing the os module for file and directory operations
import tkinter
from tkinter import messagebox, filedialog, simpledialog


class WikiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpylWiki")

        # Frames
        self.frame_left = tkinter.Frame(root)
        self.frame_left.pack(side=tkinter.LEFT, fill=tkinter.Y, pady=5)

        self.frame_top = tkinter.Frame(root)
        self.frame_top.pack(side=tkinter.TOP, fill=tkinter.X, pady=5)

        self.frame_right = tkinter.Frame(root)
        self.frame_right.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True, pady=5)

        # Index Pane
        self.index_listbox = tkinter.Listbox(self.frame_left)
        self.index_listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.scrollbar = tkinter.Scrollbar(self.frame_left)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.index_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.index_listbox.yview)

        # Bind the listbox selection event to the load_page method
        self.index_listbox.bind("<<ListboxSelect>>", self.load_page)

        # # Search Bar
        # self.search_entry = tkinter.Entry(self.frame_top)
        # self.search_entry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        # self.search_button = tkinter.Button(self.frame_top, text="Search", command=self.search_page)
        # self.search_button.pack(side=tkinter.RIGHT)

        # Reading Pane
        self.text_area = tkinter.Text(self.frame_right)
        self.text_area.pack(fill=tkinter.BOTH, expand=True)

        # Buttons
        self.add_button = tkinter.Button(self.frame_left, text="Add Page", command=self.add_page)
        self.add_button.pack(side=tkinter.TOP, fill=tkinter.X)

        self.save_button = tkinter.Button(self.frame_left, text="Save Page", command=self.save_page)
        self.save_button.pack(side=tkinter.TOP, fill=tkinter.X)

        self.delete_button = tkinter.Button(self.frame_left, text="Delete Page", command=self.delete_page)
        self.delete_button.pack(side=tkinter.TOP, fill=tkinter.X)

        # Create a directory for storing pages if it doesn't exist
        self.pages_dir = "pages"
        if not os.path.exists(self.pages_dir):
            os.makedirs(self.pages_dir)

        # Load existing pages into the listbox
        self.load_pages()

    def load_pages(self):
        """Load all existing pages into the listbox."""
        self.index_listbox.delete(0, tkinter.END)
        for filename in os.listdir(self.pages_dir):
            if filename.endswith(".txt"):
                title = filename[:-4]  # Remove the .txt extension
                self.index_listbox.insert(tkinter.END, title)

    # def search_page(self):
    #     pass  # Placeholder for search functionality

    def add_page(self):
        # Prompt for the page title
        title = simpledialog.askstring("Add Page", "Enter the page title:")
        if title:
            # Check if the page already exists
            filename = os.path.join(self.pages_dir, f"{title}.txt")
            if os.path.exists(filename):
                messagebox.showwarning("Add Page", "A page with this title already exists.")
                return

            # Create an empty file for the new page
            with open(filename, "w") as file:
                file.write("")  # Create an empty file

            # Add the title to the listbox and load the page
            self.index_listbox.insert(tkinter.END, title)
            self.index_listbox.select_set(tkinter.END)  # Select the newly added page
            self.load_page()


    # def search_page(self):
    #     """Search for pages and update the listbox based on the search term."""
    #     search_term = self.search_entry.get()
    #     print(f"Search term: {search_term}")
    #     self.load_pages(search_term)
        
    # def load_pages(self, search_term=""):
    #     """Load all existing pages into the listbox, optionally filtering by a search term."""
    #     self.index_listbox.delete(0, tkinter.END)
    #     print(f"Loading pages with search term: {search_term}")
    #     for filename in os.listdir(self.pages_dir):
    #         if filename.endswith(".txt"):
    #             title = filename[:-4]  # Remove the .txt extension
    #             if search_term.lower() in title.lower():  # Case-insensitive search
    #                 self.index_listbox.insert(tkinter.END, title)
    #                 print(f"Matching page found: {title}")

    def load_page(self, event=None):
        """Load the selected page's content into the text area."""
        selected_index = self.index_listbox.curselection()
        if selected_index:
            title = self.index_listbox.get(selected_index)
            filename = os.path.join(self.pages_dir, f"{title}.txt")
            with open(filename, "r") as file:
                content = file.read()
            self.text_area.delete(1.0, tkinter.END)
            self.text_area.insert(tkinter.END, content)

    def save_page(self):
        """Save the content of the text area to the selected file."""
        selected_index = self.index_listbox.curselection()
        if selected_index:
            title = self.index_listbox.get(selected_index)
            filename = os.path.join(self.pages_dir, f"{title}.txt")
            content = self.text_area.get(1.0, tkinter.END)
            with open(filename, "w") as file:
                file.write(content)
            messagebox.showinfo("Save Page", "Page saved successfully.")
        else:
            messagebox.showwarning("Save Page", "No page selected.")


    def delete_page(self):
        selected_index = self.index_listbox.curselection()
        if selected_index:
            title = self.index_listbox.get(selected_index)
            response = messagebox.askyesno("Delete Page", f"Are you sure you want to delete '{title}'?")
            if response:
                filename = os.path.join(self.pages_dir, f"{title}.txt")
                if os.path.exists(filename):
                    os.remove(filename)
                    self.index_listbox.delete(selected_index)
                    self.text_area.delete(1.0, tkinter.END)
                    messagebox.showinfo("Delete Page", "Page deleted successfully.")
        else:
            messagebox.showwarning("Delete Page", "No page selected.")


if __name__ == "__main__":
    root = tkinter.Tk()
    app = WikiApp(root)
    root.mainloop()
