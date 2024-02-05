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

const moodToEmoji = {
  '-2': '😢',
  '-1': '☹️',
  '0': '😐',
  '1': '🙂',
  '2': '🤩',
};
