const API_BASE = '/api';

const selectors = {
  messageForm: document.getElementById('message-form'),
  messageAuthor: document.getElementById('message-author'),
  messageContent: document.getElementById('message-content'),
  messageList: document.getElementById('message-list'),
  postForm: document.getElementById('post-form'),
  postTitle: document.getElementById('post-title'),
  postBody: document.getElementById('post-body'),
  postList: document.getElementById('post-list'),
  todoForm: document.getElementById('todo-form'),
  todoDescription: document.getElementById('todo-description'),
  todoList: document.getElementById('todo-list'),
  groceryForm: document.getElementById('grocery-form'),
  groceryName: document.getElementById('grocery-name'),
  groceryQuantity: document.getElementById('grocery-quantity'),
  groceryList: document.getElementById('grocery-list'),
  ingredientForm: document.getElementById('ingredient-form'),
  ingredientName: document.getElementById('ingredient-name'),
  ingredientAmount: document.getElementById('ingredient-amount'),
  ingredientLocation: document.getElementById('ingredient-location'),
  ingredientList: document.getElementById('ingredient-list'),
  recognitionForm: document.getElementById('recognition-form'),
  recognitionImage: document.getElementById('recognition-image'),
  recognitionStatus: document.getElementById('recognition-status'),
  itemTemplate: document.getElementById('item-template'),
};

const formatDate = (value) => new Date(value).toLocaleString();

const createButton = (label, variant = 'primary') => {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.textContent = label;
  if (variant === 'danger') {
    btn.style.background = 'linear-gradient(135deg, #ef4444, #b91c1c)';
  } else if (variant === 'outline') {
    btn.style.background = 'rgba(255,255,255,0.1)';
    btn.style.color = '#2563eb';
    btn.style.border = '1px solid rgba(37, 99, 235, 0.4)';
  }
  return btn;
};

const renderList = (listElement, items, renderContent) => {
  listElement.innerHTML = '';
  items.forEach((item) => {
    const clone = selectors.itemTemplate.content.firstElementChild.cloneNode(true);
    const content = clone.querySelector('.item-content');
    const actions = clone.querySelector('.item-actions');
    renderContent(content, actions, item);
    listElement.appendChild(clone);
  });
};

async function fetchJSON(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || 'Request failed');
  }
  return response.status === 204 ? null : response.json();
}

async function refreshMessages() {
  const messages = await fetchJSON(`${API_BASE}/messages`);
  renderList(selectors.messageList, messages, (content, actions, message) => {
    content.innerHTML = `
      <strong>${message.author}</strong>
      <span class="meta">${formatDate(message.created_at)}</span>
      <span>${message.content}</span>
    `;
    const remove = createButton('Delete', 'danger');
    remove.addEventListener('click', async () => {
      await fetchJSON(`${API_BASE}/messages/${message.id}`, { method: 'DELETE' });
      refreshMessages();
    });
    actions.appendChild(remove);
  });
}

async function refreshPosts() {
  const posts = await fetchJSON(`${API_BASE}/posts`);
  renderList(selectors.postList, posts, (content, actions, post) => {
    content.innerHTML = `
      <strong>${post.title}</strong>
      <span class="meta">${formatDate(post.created_at)}</span>
      <span>${post.body}</span>
    `;
    const remove = createButton('Delete', 'danger');
    remove.addEventListener('click', async () => {
      await fetchJSON(`${API_BASE}/posts/${post.id}`, { method: 'DELETE' });
      refreshPosts();
    });
    actions.appendChild(remove);
  });
}

async function refreshTodos() {
  const todos = await fetchJSON(`${API_BASE}/todos`);
  renderList(selectors.todoList, todos, (content, actions, todo) => {
    if (todo.completed) {
      content.parentElement.classList.add('completed');
    }
    content.innerHTML = `
      <span>${todo.description}</span>
      <span class="meta">${formatDate(todo.created_at)}</span>
    `;
    const toggle = createButton(todo.completed ? 'Undo' : 'Done', 'outline');
    toggle.addEventListener('click', async () => {
      await fetchJSON(`${API_BASE}/todos/${todo.id}`, { method: 'PATCH' });
      refreshTodos();
    });
    const remove = createButton('Delete', 'danger');
    remove.addEventListener('click', async () => {
      await fetchJSON(`${API_BASE}/todos/${todo.id}`, { method: 'DELETE' });
      refreshTodos();
    });
    actions.appendChild(toggle);
    actions.appendChild(remove);
  });
}

async function refreshGroceries() {
  const groceries = await fetchJSON(`${API_BASE}/groceries`);
  renderList(selectors.groceryList, groceries, (content, actions, grocery) => {
    if (grocery.checked) {
      content.parentElement.classList.add('completed');
    }
    content.innerHTML = `
      <span>${grocery.name}</span>
      <span class="meta">${grocery.quantity}</span>
    `;
    const toggle = createButton(grocery.checked ? 'Need' : 'Have', 'outline');
    toggle.addEventListener('click', async () => {
      await fetchJSON(`${API_BASE}/groceries/${grocery.id}`, { method: 'PATCH' });
      refreshGroceries();
    });
    const remove = createButton('Delete', 'danger');
    remove.addEventListener('click', async () => {
      await fetchJSON(`${API_BASE}/groceries/${grocery.id}`, { method: 'DELETE' });
      refreshGroceries();
    });
    actions.appendChild(toggle);
    actions.appendChild(remove);
  });
}

async function refreshIngredients() {
  const ingredients = await fetchJSON(`${API_BASE}/pantry`);
  renderList(selectors.ingredientList, ingredients, (content, actions, ingredient) => {
    content.innerHTML = `
      <span>${ingredient.name}</span>
      <span class="meta">${[ingredient.amount, ingredient.location]
        .filter(Boolean)
        .join(' • ')}</span>
    `;
    const remove = createButton('Delete', 'danger');
    remove.addEventListener('click', async () => {
      await fetchJSON(`${API_BASE}/pantry/${ingredient.id}`, { method: 'DELETE' });
      refreshIngredients();
    });
    actions.appendChild(remove);
  });
}

selectors.messageForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  await fetchJSON(`${API_BASE}/messages`, {
    method: 'POST',
    body: JSON.stringify({
      author: selectors.messageAuthor.value.trim(),
      content: selectors.messageContent.value.trim(),
    }),
  });
  selectors.messageContent.value = '';
  refreshMessages();
});

selectors.postForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  await fetchJSON(`${API_BASE}/posts`, {
    method: 'POST',
    body: JSON.stringify({
      title: selectors.postTitle.value.trim(),
      body: selectors.postBody.value.trim(),
    }),
  });
  selectors.postTitle.value = '';
  selectors.postBody.value = '';
  refreshPosts();
});

selectors.todoForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  await fetchJSON(`${API_BASE}/todos`, {
    method: 'POST',
    body: JSON.stringify({ description: selectors.todoDescription.value.trim() }),
  });
  selectors.todoDescription.value = '';
  refreshTodos();
});

selectors.groceryForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  await fetchJSON(`${API_BASE}/groceries`, {
    method: 'POST',
    body: JSON.stringify({
      name: selectors.groceryName.value.trim(),
      quantity: selectors.groceryQuantity.value.trim() || '1',
    }),
  });
  selectors.groceryName.value = '';
  selectors.groceryQuantity.value = '1';
  refreshGroceries();
});

selectors.ingredientForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  await fetchJSON(`${API_BASE}/pantry`, {
    method: 'POST',
    body: JSON.stringify({
      name: selectors.ingredientName.value.trim(),
      amount: selectors.ingredientAmount.value.trim(),
      location: selectors.ingredientLocation.value.trim(),
    }),
  });
  selectors.ingredientName.value = '';
  selectors.ingredientAmount.value = '';
  selectors.ingredientLocation.value = '';
  refreshIngredients();
});

selectors.recognitionForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const file = selectors.recognitionImage.files[0];
  if (!file) return;
  const data = new FormData();
  data.append('image', file);
  selectors.recognitionStatus.textContent = 'Analyzing…';
  try {
    const response = await fetch(`${API_BASE}/pantry/recognize`, {
      method: 'POST',
      body: data,
    });
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail || 'Recognition failed');
    }
    await response.json();
    selectors.recognitionStatus.textContent = 'Ingredients added from photo!';
    selectors.recognitionImage.value = '';
    refreshIngredients();
  } catch (error) {
    selectors.recognitionStatus.textContent = error.message;
  }
});

function initialize() {
  refreshMessages();
  refreshPosts();
  refreshTodos();
  refreshGroceries();
  refreshIngredients();
}

initialize();
