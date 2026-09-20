let bedroom = 3;

const taxRate = 0.08;

let price;
let result = null;

"10" == 10;
"10" === 10;

if (bedroom > 3) {
    console.log("This is a large house!");
    console.warn("Warning: This house is too big!");
} else {
    console.log("Standard house.");
}

for (let i =0; i < 5; i++) {
    console.log(i);
}   

let sample = {id: 1, name: "Sample Object", type: "Example"};

console.log(sample.name);
console.log(sample["name"]);

let arr = [1, 2, 3, 4, 5];
console.log(arr.length);

let x = document.querySelector("section p");
console.log(x.textContent);

//console.log("tieu de", title.textContent);
const title = document.querySelector("#gioi-thieu");
const content = document.querySelector("section p");
let ar = [];
let post = {
    title: title.textContent,
    content: content.textContent.trim(),};

arr.push(post);

console.log(arr);

async function greet() {
    return "Hello, World!";
}

console.log(greet());
greet().then((response) => {
    console.log(response);
});

//c2
async function getData() {
    const text = await greet();
    console.log(text);
}

getData();

// function fetchUsers() {
//     fetch("https://jsonplaceholder.typicode.com/users")
//         .then((response) => {
//             return response.json();
//         })
//         .then((users) => {
//             let tableBody = document.querySelector("#user-table tbody");
//             users.forEach((user) => {
//                 const row = document.createElement("tr");
//                 row.innerHTML = `
//                     <td>${user.id}</td>
//                     <td>${user.name}</td>
//                     <td>${user.email.toLowerCase()}</td>
//                     <td>${user.phone}</td>
//                     <td>${user.website}</td>
//                     <td>${user.address.city + "-" + user.address.street}</td>
//                 `;
//                 tableBody.appendChild(row);
//             });
//         })
// }

// fetchUsers o dang async/await
async function fetchUsers() {
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/users");
        const users = await response.json();

        const table = document.querySelector("#user-table tbody");
        users.forEach(function(user) {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email.toLowerCase()}</td>
                <td>${user.phone}</td>
                <td>${user.website}</td>
                <td>${user.address.city + "-" + user.address.street}</td>
            `;
            table.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching users:", error);
    }
}

async function fetchBackendMessage() {
    try {
        const response = await fetch("/api/message");
        const data = await response.json();
        console.log("Backend message:", data);
    } catch (error) {
        console.error("Error fetching backend message:", error);
    }
}

fetchUsers();
fetchBackendMessage();