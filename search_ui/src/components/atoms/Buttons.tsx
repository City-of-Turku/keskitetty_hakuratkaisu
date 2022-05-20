import styled from 'styled-components'

export const RedButton = styled.button<{ accentColor: string }>`
  font-size: 1em;
  font-weight: 700;
  height: 47px;
  padding: 0 16px;
  background-color: ${p => p.accentColor};
  color: #fff;
  border: 0;
  border-radius: 3px;
  cursor: pointer;
  transition: .5s;
  &:hover {
    box-shadow: 0 0 16px rgba(0, 0, 0, .6);
  }
  &:disabled {
    opacity: 0.2;
  }  
`

export const WhiteButton = styled(RedButton)`
  background-color: #fff;
  color: rgba(0, 0, 0, .7);
  border: 1px solid rgba(0, 0, 0, 0.7);
  font-weight: 400;
`

export const SearchButton = styled(RedButton).attrs({className: 'kehauicss-search-button'})`
  display: flex;
  align-items: center;
  svg {
    padding-left: 6px;
  }
`

export const NudeButton = styled.button`
  border: 0;
  background: transparent;
  font: inherit;
  padding: 0;
  margin: inherit;
  cursor: pointer;
  &:hover {
    text-decoration: underline;
  }
`