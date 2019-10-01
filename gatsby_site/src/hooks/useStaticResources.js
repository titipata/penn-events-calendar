import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faBookmark, faCalendarAlt, faChevronCircleDown,
  faChevronCircleUp, faClock, faCopy, faExternalLinkAlt,
  faFileAlt, faMapMarkerAlt, faSchool,
  faStar, faUniversity, faUserTie, faSearch,
} from '@fortawesome/free-solid-svg-icons';
import { useState, useEffect } from 'react';
import 'rc-pagination/assets/index.css';

function useStaticResources() {
  const [icons, setIcons] = useState([
    faCalendarAlt, faMapMarkerAlt, faClock, faFileAlt,
    faExternalLinkAlt, faUserTie, faSchool, faUniversity,
    faBookmark, faChevronCircleDown, faChevronCircleUp,
    faCopy, faStar, faSearch,
  ]);

  useEffect(() => {
    // add fa font to use
    library.add(...icons);
  }, [icons]);

  // return a function to add icon
  return icon => setIcons([...icons, icon]);
}

export default useStaticResources;
