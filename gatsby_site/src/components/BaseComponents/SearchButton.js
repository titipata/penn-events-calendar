import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import styled, { keyframes, css } from 'styled-components';
import { slideInRight } from 'react-animations';
import { Key } from '../../utils';

const Container = styled.div`
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

  ${props => props.active && css`
    width: 100%;
    display: block;
    /* animation */
    animation: 0.5s ${props.active && slideInAnimation} forwards;
  `}
`;

const SuggestionList = styled.ul`
  list-style: none;
  position: absolute;
  top: 45px;
  right: 0;
  background-color: white;
  margin: 0;
  max-height: 250px;
  overflow: scroll;
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
  border: 1px solid #ddd;
  width: 120%;
  border-radius: 2px;
  ${props => props.hidden && css`
    display: none;
  `}
`;

const SuggestionItem = styled.li`
  height: 50px;
  display: flex;
  align-items: center;
  margin: 0;
  padding: 5px 15px;

  & :hover {
    background-color: rgba(50, 50, 50, 0.1);
    cursor: pointer;
  }
`;

const TextWrapper = styled.span`
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
      <SuggestionList
        hidden={suggestionList.length === 0 || !searchQuery}
      >
        {suggestionList.slice(0, 10).map(item => (
          <SuggestionItem
            onClick={() => setSearchQuery(item)}
            key={Key.getShortKey()}
          >
            <TextWrapper>
              {item}
            </TextWrapper>
          </SuggestionItem>
        ))}
      </SuggestionList>
    </Container>
  );
};

export default SearchButton;
