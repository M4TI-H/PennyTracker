export default async function fetchAccounts(user) {
  try {
    const url = new URL("http://localhost:8000/transactions/fetch_accounts");
    url.searchParams.append("user_id", user);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching accounts data: ${error}`);
  }
}