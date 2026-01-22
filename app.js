const app = document.getElementById("app");

function router() {
  const path = window.location.pathname;
  const parts = path.split("/").filter(Boolean);

  if (parts[0] === "f" && parts[2] === "p") {
    const community = parts[1];
    const id = parts[3];

    renderPost(community, id);
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

function renderPost(community, id) {
  const post = POSTS.find(p => p.id === id && p.community === community);

  if (!post) {
    app.innerHTML = "<h2>Post not found</h2>";
    return;
  }

  let optionsHTML = post.options
    .map(opt => `<div class="poll-option">${opt}</div>`)
    .join("");

  app.innerHTML = `
    <h4>f/${community}</h4>
    <h2>${post.title}</h2>
    ${optionsHTML}
  `;
}

window.addEventListener("popstate", router);
router();
