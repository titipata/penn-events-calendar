import { useState, useEffect, useRef } from 'react';

function useNodeHeight() {
  const [height, setHeight] = useState(0);
  const ref = useRef(null);

  useEffect(() => {
    setHeight(ref.current.clientHeight);
  }, []);

  return height;
}

export default useNodeHeight;
