import React, { useEffect, useState } from 'react';

function formatEvent(event) {
  const date = new Date(event.timestamp);
  const formattedDate = date.toLocaleString('en-US', { timeZone: 'UTC', hour12: true, day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  if (event.action === 'PUSH') {
    return `${event.author} pushed to ${event.to_branch} on ${formattedDate} UTC`;
  }
  if (event.action === 'PULL_REQUEST') {
    return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${formattedDate} UTC`;
  }
  if (event.action === 'MERGE') {
    return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${formattedDate} UTC`;
  }
  return 'Unknown event';
}

export default function EventsFeed() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchEvents = async () => {
    try {
      const res = await fetch('http://localhost:5001/api/events');
      const data = await res.json();
      setEvents(data.events || []);
    } catch (err) {
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-xl mx-auto mt-10 p-4 bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-4 text-center">Repo Activity Feed</h1>
      {loading ? (
        <div className="text-center text-gray-500">Loading...</div>
      ) : events.length === 0 ? (
        <div className="text-center text-gray-400">No events yet.</div>
      ) : (
        <ul className="space-y-3">
          {events.map(event => (
            <li key={event._id} className="p-3 border rounded bg-gray-50">
              {formatEvent(event)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
} 