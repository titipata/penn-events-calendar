import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import styled, { keyframes, css } from 'styled-components';
import { slideInRight } from 'react-animations';

const Container = styled.div`
  width: 35%;
  margin-bottom: 1.56rem;
  display: flex;
  align-items: center;
  justify-content: flex-end;
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

  ${props => props.active && css`
    width: 100%;
    display: block;
    /* animation */
    animation: 0.5s ${props.active && slideInAnimation} forwards;
  `}
`;

const SuggestionList = styled.ul`
  width: auto;
  list-style: none;
  position: absolute;
  top: 0;
  right: 0;
`;

const SuggestionItem = styled.li`
  height: 20px;
`;

const fetcher = (kw, setter) => fetch(`http://localhost:8888/suggestion?text=${kw}`)
  .then(res => res.json())
  .then((resJson) => {
    console.log(resJson);
    setter(resJson);
  });

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
    inputRef.current.focus();

    if (searchQuery) {
      fetcher(searchQuery, setSuggestionList);
    }
  }, [active, searchQuery]);

  return (
    <Container>
      <StyledFa
        icon="search"
        onClick={() => {
          setActive(!active);
        }}
      />
      <StyledInput
        type="text"
        value={searchQuery}
        onChange={handleQueryChange}
        active={active}
        ref={inputRef}
      />
      <SuggestionList>
        {suggestionList.slice(0, 10).map(item => (
          <SuggestionItem
            onClick={() => setSearchQuery(item)}
          >
            {item}
          </SuggestionItem>
        ))}
      </SuggestionList>
    </Container>
  );
};

export default SearchButton;
