export default function getMonthName(month: string) {
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];
  return monthNames[parseInt(month, 10) - 1];
}