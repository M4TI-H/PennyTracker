export default function formatDate(date) {
  const dateOptions = {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
  };

  return date.toLocaleString("en-GB", dateOptions).replace(',', '');;
}