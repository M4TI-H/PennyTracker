export async function fetchData<FetchType>(url: string, options?: any): Promise<{ data?: FetchType; error?: string }> {
    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      const data = (await response.json()) as FetchType;
      return { data };
    }
    catch (error: any) {
      return { error: error.message };
    }
  }
  