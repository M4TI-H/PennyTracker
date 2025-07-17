export default async function fetchExpenseCategories(user: number) {
  try {
    const url = new URL("http://localhost:8000/transactions/expense_categories");
    url.searchParams.append("user_id", user.toString());

    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching categories data: ${error}`);
  }
}