import React, { useState } from "react";

export default function Analysis({ analyticData }) {
  const [visualiseData, setVisualiseData] = useState(analyticData);

  const getDomainName = () => {
    let tmpVal = analyticData[0].URL.split(".");
    console.log(tmpVal);
    tmpVal = `https://${tmpVal[1]}.${tmpVal[2]}`;
    return tmpVal;
  };
  const domainName = getDomainName();
  const s3HostedSites = analyticData.filter((x) => {
    if (x.Status == "Exists" || x.Status == "PUBLIC" || x.Status == "PRIVATE") {
      return x;
    }
  });
  const s3Buckets = analyticData.filter((x) => {
    if (x.Status == "PUBLIC" || x.Status == "PRIVATE") {
      return x;
    }
  });
  const handleStatClick = (data) => {
    setVisualiseData(data);
  };

  const getTableBg = (status) => {
    if (status == "PUBLIC") {
      return "bg-emerald-800";
    }
    if (status == "PRIVATE") {
      return "bg-rose-800";
    }
    if (status == "Exists") {
      return "bg-purple-800";
    }
  };

  return (
    <div className="flex flex-col overflow-auto">
      <div className="self-center my-4 text-4xl">
        S3 Bucket Analysis : <span className="font-bold">{domainName}</span>
      </div>
      <div className="bg-bg-dark-accent flex justify-around p-4">
        <div
          className="flex flex-col text-center cursor-pointer"
          onClick={() => {
            handleStatClick(analyticData);
          }}
        >
          <div className="font-semibold text-xl">Total Urls</div>
          <div className="text-3xl">{analyticData.length}</div>
        </div>
        <div
          className="flex flex-col text-center cursor-pointer"
          onClick={() => {
            handleStatClick(s3HostedSites);
          }}
        >
          <div className="font-semibold text-xl">S3 Hosted Sites</div>
          <div className="text-3xl">{s3HostedSites.length}</div>
        </div>
        <div
          className="flex flex-col text-center cursor-pointer"
          onClick={() => {
            handleStatClick(s3Buckets);
          }}
        >
          <div className="font-semibold text-xl">S3 Buckets</div>
          <div className="text-3xl">{s3Buckets.length}</div>
        </div>
      </div>
      <table
        className="m-4 width-screen content-center table-auto "
        rules="rows"
      >
        <thead className="text-xl font-semibold border-b">
          <td className="px-2 py-4">Status</td>
          <td className="px-2 py-4">URL</td>
          <td className="px-2 py-4">Bucket URL</td>
        </thead>
        {visualiseData.map((row) => {
          let trbg = getTableBg(row.Status);
          return (
            <tr className={`hover:bg-bg-dark-accent ${trbg}`}>
              <td className="p-2">{row.Status}</td>
              <td
                className="p-2 cursor-pointer"
                onClick={() => {
                  window.location.href = row.URL;
                }}
              >
                {row.URL}
              </td>
              <td
                className="p-2 cursor-pointer"
                onClick={() => {
                  window.location.href = row["Bucket Url"];
                }}
              >
                {row["Bucket Url"]}
              </td>
            </tr>
          );
        })}
      </table>
    </div>
  );
}
