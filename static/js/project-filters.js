(function () {
  const topic = document.getElementById('project-topic');
  const sort = document.getElementById('project-sort');
  if (!topic || !sort) return;
  const lists = Array.from(document.querySelectorAll('.past-project-list'));
  lists.forEach(list => {
    Array.from(list.children).forEach((item, index) => { item.dataset.dateOrder = index; });
  });
  const requested = new URLSearchParams(window.location.search).get('topic');
  if (Array.from(topic.options).some(option => option.value === requested)) topic.value = requested;

  function update() {
    let total = 0;
    lists.forEach(list => {
      const items = Array.from(list.children);
      items.sort((a, b) => sort.value === 'title'
        ? a.dataset.projectTitle.localeCompare(b.dataset.projectTitle)
        : Number(a.dataset.dateOrder) - Number(b.dataset.dateOrder));
      let visible = 0;
      items.forEach(item => {
        item.hidden = Boolean(topic.value) && !item.dataset.projectTopics.split(' ').includes(topic.value);
        if (!item.hidden) visible++;
        list.appendChild(item);
      });
      list.closest('section').hidden = visible === 0;
      total += visible;
    });
    document.getElementById('project-filter-result').textContent = total === 0
      ? 'No projects match this topic.'
      : total + (total === 1 ? ' project' : ' projects');
  }
  topic.addEventListener('change', update);
  sort.addEventListener('change', update);
  update();
}());
