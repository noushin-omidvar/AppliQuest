document.addEventListener("DOMContentLoaded", async function () {
  const userId = localStorage.getItem("user_id");

  resp = await axios.get(`api/v1/users/${userId}/jobs`);
  data = resp.data.jobs;
  const statuses = ["Wishlist", "Applied", "Interview", "Offer", "Rejected"];

  const statusCounts = {
    Wishlist: 0,
    Applied: 0,
    Interview: 0,
    Offer: 0,
    Rejected: 0,
  };
  for (let i = 0; i < data.length; i++) {
    const status = data[i].status;
    statusCounts[status]++;
  }

  const sortedStatusCounts = statuses.map((status) => statusCounts[status]);

  const funnelChart = document.getElementById("funnelChart").getContext("2d");
  new Chart(funnelChart, {
    type: "funnel",
    data: {
      labels: statuses,
      shrinkAnchor: "top",
      datasets: [
        {
          data: sortedStatusCounts,
          backgroundColor: [
            "#FFCE56",
            "#36A2EB",
            "#f37236",
            "#4BC0C0",
            "#FF6384",
          ],
          hoverBackgroundColor: [
            "#FFCE56",
            "#36A2EB",
            "#f37236",
            "#4BC0C0",
            "#FF6384",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        datalabels: {
          color: "#ffffff",
          font: {
            weight: "thin",
          },
          formatter: function (value, context) {
            let label = context.chart.data.labels[context.dataIndex];
            if (typeof value !== "undefined") {
              return label + ": " + value.toString();
            } else {
              return label + ": N/A";
            }
          },
        },
      },
    },
    plugins: [ChartDataLabels],
  });
});
