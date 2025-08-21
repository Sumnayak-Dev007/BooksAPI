const baseEndpoint = "http://localhost:8000/api";
const loginForm = document.getElementById("login-form");
// const searchForm = document.getElementById("search-form");
const contentContainer = document.getElementById("content-container");

// Login + store tokens
function handleLogin(event) {
    event.preventDefault();
    const loginEndpoint = `${baseEndpoint}/token/`;
    const loginFormData = new FormData(loginForm);
    const loginObjectData = Object.fromEntries(loginFormData);

    console.log("Login payload:", loginObjectData); // debug

    fetch(loginEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginObjectData)
    })
    .then(async response => {
        const data = await response.json();
        console.log("Login response:", data, "Status:", response.status);

        if (data.access && data.refresh) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            getBookstList();
        } else {
            alert("Login failed: " + (data.detail || "Invalid credentials"));
        }
    })
    .catch(error => {
        console.error("Login Error:", error);
        alert("Something went wrong during login.");
    });
}



// function handleSearch(event) {
//     event.preventDefault();

//     const formData = new FormData(searchForm);         
//     const data = Object.fromEntries(formData);         
//     let searchParams = new URLSearchParams(data);
//     const endpoint = `${baseEndpoint}/search/?${searchParams}`;
//     const accessToken = localStorage.getItem("access");

//     fetch(endpoint, {
//         method: "GET",
//         headers: {
//             "Content-Type": "application/json",
//             ...(accessToken && { Authorization: `Bearer ${accessToken}` })
//         }
//     })
//     .then(response => {
//         if (response.status === 401) {
//             return response.json().then(data => {
//                 if (data.code === "token_not_valid") {
//                     refreshTokenAndRetry(() => handleSearch(event)); // 🔁 retry after refresh
//                 } else {
//                     logout();
//                 }
//             });
//         }
//         return response.json();
//     })
//     .then(data => {
//         if (data && contentContainer) {
//             contentContainer.innerHTML = "";  

//             if (data.hits && Array.isArray(data.hits)) {
//                 if (data.hits.length > 0) {
//                     let htmlStr = "<ul>";  

//                 for (let result of data.hits) {
//             console.log("Result:", result);  
//             htmlStr += `
//                 <li style="margin-bottom: 1rem; border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
//                     <strong>${result.title ?? "No Title"}</strong><br>
//                     <small>Seller: ${result.user_username ?? "Unknown"}</small><br>
//                     Price: ₹${result.price ?? "N/A"}<br>
//                     Sale Price: ₹${result.sale_price ?? "N/A"}<br>
//                     Tags: ${Array.isArray(result._tags) ? result._tags.join(", ") : "None"}
//                 </li>
//             `;
//         }

//         htmlStr += "</ul>";  // Close the list after the loop
//         contentContainer.innerHTML = htmlStr;

//                 } else {
//                     contentContainer.innerHTML = "<p>No results found</p>";
//                 }
//             } else {
//                 contentContainer.innerHTML = "<p>No results found</p>";
//             }
//         }
//     })
//     .catch(error => {
//         console.error("Search Error:", error);
//         alert("Something went wrong during Search.");
//     });
// }


// Display Books
function writeToContainer(data) {
    if (!contentContainer) return;

    const books = data.results || data;  // handle pagination or direct array

    if (!Array.isArray(books) || books.length === 0) {
        contentContainer.innerHTML = "<p>No Books available.</p>";
        return;
    }

    contentContainer.innerHTML = ""; // clear old content

    books.forEach(book => {
        const card = document.createElement("div");
        card.className = "book-card";
        card.style.border = "1px solid #ccc";
        card.style.margin = "10px";
        card.style.padding = "10px";
        card.style.borderRadius = "8px";

        card.innerHTML = `
            <h3>${book.title}</h3>
            <p>${book.content || "No description available"}</p>
            <p><strong>Price:</strong> ₹${book.price}</p>
            <p><strong>Sale Price:</strong> ₹${book.sale_price}</p>
            <p><strong>Author:</strong> ${book.my_author_data?.author_name || "Unknown"}</p>
            ${book.image_url ? `<img src="${book.image_url}" alt="${book.title}" style="max-width:200px; display:block; margin-top:10px;" />` : ""}
        `;

        contentContainer.appendChild(card);
    });
}

//  Refresh token if access expired
function refreshTokenAndRetry(callback) {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) {
        alert("Session expired. Please log in again.");
        logout();
        return;
    }

    const refreshEndpoint = `${baseEndpoint}/token/refresh/`;

    fetch(refreshEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem("access", data.access);
            console.log("🔄 Token refreshed");
            callback(); 
        } else {
            alert("Session expired. Please log in again.");
            logout();
        }
    })
    .catch(error => {
        console.error("Refresh Error:", error);
        logout();
    });
}


function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    contentContainer.innerHTML = "<p>You have been logged out. Please log in again.</p>";
}


function getBookstList() {
    const endpoint = `${baseEndpoint}/treasure/`;
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        logout();
        return;
    }

    fetch(endpoint, {
    method: "GET",
    headers: {
        Authorization: `Bearer ${accessToken}`
    }
    })
    .then(response => {
        if (response.status === 401) {
            return response.json().then(data => {
                if (data.code === "token_not_valid") {
                    refreshTokenAndRetry(getBookstList); 
                } else {
                    logout();
                }
            });
        }
        return response.json();
    })
    .then(data => {
        if (data && !data.code) {
            writeToContainer(data);
        }
    })
    .catch(error => {
        console.error("Books Fetch Error:", error);
        contentContainer.innerHTML = "<p>Error loading Books.</p>";
    });
}

// Form listener
if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
}

// if (searchForm) {
//     searchForm.addEventListener("submit", handleSearch);
// }



async function searchBooks() {
  const query = document.getElementById("searchInput").value;
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = "Searching...";

  try {
    const response = await fetch(`http://localhost:8000/api/search/?q=${encodeURIComponent(query)}`, {
      method: "GET",
      headers: {
        "Content-Type": "multipart/form-data",
      }
    });

    const data = await response.json();
    console.log("API response data:", data);

    const Books = data.results || data;  // handle paginated or direct list
    if (!Array.isArray(Books)) {
      throw new Error("Invalid data format: Expected an array of Books");
    }

    resultsContainer.innerHTML = "";

    if (Books.length === 0) {
      resultsContainer.innerHTML = "<p>No results found.</p>";
      return;
    }

    Books.forEach(Book => {
      const card = document.createElement("div");
      card.className = "Book-card";
      card.innerHTML = `
        <h3>${Book.title}</h3>
        <p>${Book.content || "No description available"}</p>
        <p><strong>Price:</strong> $${Book.price}</p>
      `;
      resultsContainer.appendChild(card);
    });

  } catch (error) {
    console.error("Search Error:", error);
    resultsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}

window.searchBooks = searchBooks;


// const { liteClient: algoliasearch } = window['algoliasearch/lite'];
// const searchClient = algoliasearch('8H1FCJWZWP', '5e9169fbedbbfbfc7aefa0e37712812a');


// const search = instantsearch({
//   indexName: 'suman_Book',
//   searchClient,
// });

// search.addWidgets([
//   instantsearch.widgets.searchBox({
//     container: '#searchbox',
//   }),

//   instantsearch.widgets.clearRefinements({
//     container: '#clear-refinements'
//   }),

//   instantsearch.widgets.refinementList({
//   container: "#user-list",
//   attribute: 'user_username'
// }),


//   instantsearch.widgets.hits({
//     container: '#hits',
//     templates: {
//       item: `<div>
//       <div>
//         <b>{{#helpers.highlight}}{"attribute" : "title"}{{/helpers.highlight}}</b>
//       </div>
//         <p>{{#helpers.highlight}}{"attribute" : "content"}{{/helpers.highlight}}</p>
//         <p>Seller: {{user_username}}</p>
//         <p>₹{{price}}</p>
//       </div>`
//     }
//   })
// ]);

// search.start();