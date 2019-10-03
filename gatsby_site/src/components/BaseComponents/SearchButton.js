import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import { navigate } from '@reach/router';
import { Link } from 'gatsby';
import React, { useEffect, useRef, useState } from 'react';
import { slideInRight } from 'react-animations';
import styled, { css, keyframes } from 'styled-components';
import { Key } from '../../utils';

const Container = styled.form`
  height: 40px;
  width: 35%;
  margin-bottom: 1.56rem;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  position: relative;
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

const slideInAnimation = keyframes`${slideInRight}`;

const StyledInput = styled.input`
  width: 0;
  display: none;
  outline: none;
  border: none;
  border-bottom: 2px solid #333;
  padding: 0 5px;

  ${props => props.active
    && css`
      width: 100%;
      display: block;
      /* animation */
      animation: 0.5s ${props.active && slideInAnimation} forwards;
    `}
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
  height: 100%;
  display: flex;
  flex: 1;
  align-items: center;
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
  color: #333;
`;

const getSuggestions = (keyword, callback) => {
  if (!keyword) return;
  fetch(`http://localhost:8888/suggestion?text=${keyword}`)
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

  const handleQueryChange = (event) => {
    setSearchQuery(event.target.value);
  };

  useEffect(() => {
    // ref should be used in effect
    if (inputRef) {
      inputRef.current.focus();
    }
  }, [active]);

  useEffect(() => {
    getSuggestions(searchQuery, setSuggestionList);
  }, [searchQuery]);

  return (
    <Container
      onSubmit={(e) => {
        e.preventDefault();
        console.log(searchQuery);
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
        onClick={() => {
          setActive(!active);
        }}
      />
      <StyledInput
        name="search_query"
        type="text"
        value={searchQuery}
        onChange={handleQueryChange}
        active={active}
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
            // onClick={() => setSearchQuery(item)}
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
            </StyledLink>
          </SuggestionItem>
        ))}
      </SuggestionList>
    </Container>
  );
};

export default SearchButton;
