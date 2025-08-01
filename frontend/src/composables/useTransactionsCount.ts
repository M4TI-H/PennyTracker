export async function fetchTransactionsCount(user_id: number) {
   try {
    const url = new URL("http://localhost:8000/transactions/transactions_count/");
    url.searchParams.append("user_id", user_id.toString());
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching transactions data: ${error}`);
  }
}