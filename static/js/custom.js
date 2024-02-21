const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  const currentDate = new Date();
  const yesterday = new Date(currentDate);
  yesterday.setDate(currentDate.getDate() - 1);

  if (date.toDateString() === currentDate.toDateString()) {
    return 'Today';
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday';
  } else {
    const options = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    };

    return new Intl.DateTimeFormat(undefined, options).format(date);
  }
};

const moodToIcon = {
  '-2': 'fa-regular fa-face-sad-tear ',
  '-1': 'fa-regular fa-face-frown ',
  '0': 'fa-regular fa-face-meh ',
  '1': 'fa-regular fa-face-smile ',
  '2': 'fa-regular fa-face-grin-stars',
};

const moodToColor = {
  '-2': 'bg-cinnabar-500',
  '-1': 'bg-navajo-500',
  '0': 'bg-primary-500',
  '1': 'bg-zomp-500',
  '2': 'bg-naples-500',
}
