import React from "react";
import { Box, Checkbox, CheckboxGroup, VStack } from "@chakra-ui/react";

interface DocumentSelectProps {
  selectedDocuments: number[];
  onSelect: (documents: number[]) => void;
}

const DocumentSelect: React.FC<DocumentSelectProps> = ({ selectedDocuments, onSelect }) => {
  const handleDocumentChange = (documents: number[]) => {
    onSelect(documents);
  };

  return (
    <Box>
      <CheckboxGroup value={selectedDocuments} onChange={handleDocumentChange}>
        <VStack align="start">
          <Checkbox value={1}>Document 1</Checkbox>
          <Checkbox value={2}>Document 2</Checkbox>
          <Checkbox value={3}>Document 3</Checkbox>
        </VStack>
      </CheckboxGroup>
    </Box>
  );
};

export default DocumentSelect;
