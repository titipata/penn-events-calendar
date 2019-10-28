import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import { navigate } from '@reach/router';
import { Link } from 'gatsby';
import React, { useEffect, useRef, useState } from 'react';
import styled, { css, keyframes } from 'styled-components';
import { Key } from '../../utils';
import { media } from '../../utils/ui';

const Container = styled.form`
  height: 40px;
  width: 35%;
  margin-bottom: 1.56rem;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  position: relative;

  ${media.medium`
    width: 80%;
  `}
`;

const StyledFa = styled(Fa)`
  font-size: 2.5rem;
  padding: 8px;

  & :hover {
    color: #333;
    background-color: #eee;
    border-radius: 50%;
    cursor: pointer;
  }

  & :active {
    color: #333;
    background-color: #ccc;
  }
`;

const slideInAnimation = keyframes`
  0% {
    width: 0%;
    opacity: 0;
  }
  100% {
    width: 100%;
    opacity: 1;
  }
`;

const slideOutAnimation = keyframes`
  0% {
    width: 100%;
    opacity: 1;
  }
  100% {
    width: 0%;
    opacity: 0;
  }
`;

const StyledInput = styled.input`
  width: 0;
  opacity: 0;
  outline: none;
  border: none;
  border-bottom: 2px solid #333;
  padding: 0 5px;

  ${props => (props.active
    ? css`
      animation: 0.45s ${slideInAnimation} ease-out forwards;
    `
    : css`
      animation: ${props.hideDuration}s ${slideOutAnimation} ease-in forwards;
    `)}
`;

const SuggestionList = styled.ul`
  background-color: white;
  list-style: none;
  position: absolute;
  top: 45px;
  right: 0;
  margin: 0;
  border: 1px solid #ddd;
  border-radius: 2px;
  width: 120%;
  max-height: 250px;
  overflow-y: auto;
  overflow-x: hidden;
  ::-webkit-scrollbar {
    width: 3px;
  }
  ::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb {
    background: #666;
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #333;
  }
  ${props => props.hidden && css`
    display: none;
  `}
`;

const SuggestionItem = styled.li`
  height: 50px;
  margin: 0;

  & :hover {
    background-color: rgba(50, 50, 50, 0.1);
  }

  & :active {
    background-color: rgba(50, 50, 50, 0.25);
  }
`;

const StyledLink = styled(Link)`
  color: #333;
  height: 100%;
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: space-between;
  padding: 5px 15px;

  & :hover {
    text-decoration: none;
  }
`;

const TextWrapper = styled.span`
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const FillerIcon = styled(StyledFa).attrs(() => ({
  icon: 'arrow-up',
  transform: { rotate: 45 },
}))`
  height: auto;
  font-size: 2.1rem;
  font-weight: lighter;
  color: #555;

  & :hover {
    border-radius: 0;
    background-color: #fff;
  }

  & :active {
    background-color: #555;
    color: #eee;
  }
`;

const getSuggestions = (suggestionUrl, callback) => {
  if (!suggestionUrl) return;
  fetch(suggestionUrl)
    .then(res => res.json())
    .then((resJson) => {
      callback(resJson);
    });
};

const SearchButton = () => {
  const inputRef = useRef(null);
  const [active, setActive] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestionList, setSuggestionList] = useState([]);
  const [hideDuration, setHideDuration] = useState(0);

  const handleQueryChange = (event) => {
    setSearchQuery(event.target.value);
  };

  useEffect(() => {
    // ref should be used in effect
    if (inputRef) {
      inputRef.current.focus();
    }

    // set hide duration
    const timeoutRef = setTimeout(() => {
      setHideDuration(0.4);
    }, 1500);

    return () => clearTimeout(timeoutRef);
  }, [active]);

  useEffect(() => {
    if (!searchQuery) return;
    const url = `/api/suggestion?text=${searchQuery}`;
    getSuggestions(url, setSuggestionList);
  }, [searchQuery]);

  return (
    <Container
      onSubmit={(e) => {
        e.preventDefault();
        navigate(`/search?search_query=${searchQuery}`);
        setActive(false);
      }}
      autoComplete="off"
      onBlur={(e) => {
        // https://gist.github.com/pstoica/4323d3e6e37e8a23dd59
        const { currentTarget } = e;
        setTimeout(() => {
          if (!currentTarget.contains(document.activeElement)) {
            setActive(false);
          }
        }, 0);
      }}
    >
      <StyledFa
        icon="search"
        onClick={() => setActive(true)}
      />
      <StyledInput
        name="search_query"
        type="text"
        value={searchQuery}
        onChange={handleQueryChange}
        active={active}
        hideDuration={hideDuration}
        ref={inputRef}
      />
      <SuggestionList
        hidden={
          suggestionList.length === 0
          || !searchQuery
          || !active
        }
      >
        {suggestionList.slice(0, 10).map(item => (
          <SuggestionItem
            key={Key.getShortKey()}
          >
            <StyledLink
              to={`/search?search_query=${item}`}
              onClick={() => {
                setActive(false);
                // should we also reset query string?
                // setSearchQuery('');
              }}
            >
              <TextWrapper>{item}</TextWrapper>
              <FillerIcon
                onClick={(e) => {
                  // manage event
                  e.stopPropagation();
                  e.preventDefault();
                  // this click behavior
                  setSearchQuery(item);
                  inputRef.current.focus();
                }}
              />
            </StyledLink>
          </SuggestionItem>
        ))}
      </SuggestionList>
    </Container>
  );
};

export default SearchButton;
