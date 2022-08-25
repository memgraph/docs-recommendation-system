import React, { useEffect, useRef } from 'react';
import * as d3 from "d3";

export const useD3 = (renderGraph) => {
  const ref = useRef();

  useEffect(() => {
    renderGraph(d3.select(ref.current));

    return () => {};
  });

  return ref;
};