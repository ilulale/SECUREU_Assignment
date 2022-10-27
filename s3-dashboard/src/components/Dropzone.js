import React, { useEffect } from "react";
import { useDropzone } from "react-dropzone";
import Papa from "papaparse";

export default function Dropzone({ setAnalData }) {
  const { acceptedFiles, getRootProps, getInputProps } = useDropzone({
    accept: {
      "text/csv": [".csv"],
    },
  });

  useEffect(() => {
    console.log(acceptedFiles[0]);
    if (acceptedFiles[0]) {
      const reader = new FileReader();
      reader.onload = async ({ target }) => {
        const csv = Papa.parse(target.result, { header: true });
        const parsedData = csv?.data;
        setAnalData(parsedData);
      };
      reader.readAsText(acceptedFiles[0]);
    }
  }, [acceptedFiles]);

  return (
    <section
      className={`border-dashed border-2 border-white w-1/2 h-1/2 self-center flex flex-col justify-center`}
    >
      <div {...getRootProps({ className: "dropzone" })}>
        <input {...getInputProps()} />
        <p className="cursor-pointer">
          Drag 'n' drop <b>output.csv</b> here, or click to select file
        </p>
      </div>
    </section>
  );
}
