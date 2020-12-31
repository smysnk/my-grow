import { useEffect, useState } from 'react';

export default function useInterval(ws) {
  const [data, setData] = useState('');

  useEffect(() => {
    ws.onmessage = (evt) => {
      if (evt.type !== 'message') {
        return;
      }
      const data = JSON.parse(evt.data);
      setData(data);
    };
  }, [ws]);

  return {
    data
  };
}