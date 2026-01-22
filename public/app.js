const app = document.getElementById("app");

async function router() {
  const parts = window.location.pathname.split("/").filter(Boolean);

  if (parts[0] === "f" && parts[2] === "p") {
    const community = parts[1];
    const id = parts[3];

    loadPost(community, id);
    return;
  }

  renderHome();
}

function renderHome() {
  app.innerHTML = `
    <h2>Welcome to Forum</h2>
    <p>Select a community.</p>
  `;
}

async function loadPost(community, id) {
  const res = await fetch(`/api/post/${id}`);
  if (!res.ok) {
    app.innerHTML = "<h2>Post not found</h2>";
    return;
  }

  const post = await res.json();

  if (post.community !== community) {
    app.innerHTML = "<h2>Wrong community</h2>";
    return;
  }

  renderPost(post);
}

function renderPost(post) {
  const options = post.options
    .map(o => `<div class="poll-option">${o}</div>`)
    .join("");

  app.innerHTML = `
    <h4>f/${post.community}</h4>
    <h2>${post.title}</h2>
    ${options}
  `;
}

window.addEventListener("popstate", router);
router();
