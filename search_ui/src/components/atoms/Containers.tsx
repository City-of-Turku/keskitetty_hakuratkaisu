import styled from 'styled-components'
import { Breakpoint } from '../../Constants'

export const ContentContainer = styled.div<{ widget: boolean }>`
  width: ${p => p.widget ? '800px' : '100%'};
  max-width: 100%;
  margin: 0 auto;
`

export const FlexContentContainer = styled(ContentContainer)`
  display: flex;
  align-items: center;
`

export const HideMobile = styled.div`
  @media (max-width: ${Breakpoint.Small}) {
    display: none;
  }
`

export const OnlyMobile = styled.div`
  display: none;
  @media (max-width: ${Breakpoint.Small}) {
    display: block;
  }
`