import { useRef } from "react";

function FileUpload({ onFileUpload }) {

   // Create a reference to the hidden file input element
  const fileInputRef = useRef();


  // Triggered when a file is selected
  const handleChange = (e) => {
    const file = e.target.files[0]; // get the first slected file
    if (file) {
      onFileUpload(file); // pass file to parent component while callback
    }
  };

  return (
    <div className="my-2">
       {/* Button to open the file picker */}
      <button
        className="px-4 py-2 bg-[var(--color-secondary)] text-black rounded-md hover:bg-[var(--color-button)] hover:text-white"
        onClick={() => fileInputRef.current.click()}
      >
        Upload File 📎
      </button>

      {/* Hidden file input element */}
      <input
        type="file"             // attach ref for programmatic click
        ref={fileInputRef}      // handle file selection
        onChange={handleChange} // accept PDF and image files
        accept=".pdf,image/*"   // hide input from UI
        className="hidden"
      />
    </div>
  );
}

export default FileUpload;