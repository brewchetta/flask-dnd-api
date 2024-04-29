import CreateContextWrapper from './_useContextState'

const [useCharacterContext, CharacterContextProvider] = CreateContextWrapper("Replace me with default state!", "exampleContextName")

export {useCharacterContext, CharacterContextProvider}
