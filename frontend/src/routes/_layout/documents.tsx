import { Container, Flex, Heading, Spinner, Table, TableContainer, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react";
import { useQuery } from "react-query";
import { createFileRoute } from "@tanstack/react-router";
import { DocumentOut } from "../../client/models/DocumentOut";
import { DocumentsService } from "../../client/services/DocumentsService";
import ActionsMenu from "../../components/Common/ActionsMenu";
import Navbar from "../../components/Common/Navbar";
import useCustomToast from "../../hooks/useCustomToast";

function Documents() {
    const showToast = useCustomToast();  // useCustomToast returns a function directly
    const {
        data: documents,
        isLoading,
        isError,
        error,
    } = useQuery<DocumentOut[]>("documents", () => DocumentsService.readDocuments({ skip: 0, limit: 100 }));

    if (isError) {
        const errDetail = error instanceof Error ? error.message : "An error occurred";
        showToast("Error loading documents", errDetail, "error");  // Correct usage of showToast
    }

    return (
        <Container maxW="full" pt="4">
            <Heading size="lg">Document Management</Heading>
            <Navbar type={"Document"} />
            {isLoading ? (
                <Flex justify="center" align="center" h="100vh">
                    <Spinner />
                </Flex>
            ) : (
                <TableContainer>
                    <Table variant="simple">
                        <Thead>
                            <Tr>
                                <Th>ID</Th>
                                <Th>Title</Th>
                                <Th>Status</Th>
                                <Th isNumeric>Actions</Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                        {documents?.map((document) => (
                            <Tr key={document.id}>
                                <Td>{document.id}</Td>
                                <Td>{document.title}</Td>
                                <Td>{document.status}</Td>
                                <Td isNumeric>
                                    <ActionsMenu type="Document" value={document} />
                                </Td>
                            </Tr>
                        ))}
                        </Tbody>
                    </Table>
                </TableContainer>
            )}
        </Container>
    );
}

// Create and export the Route for this component
export const Route = createFileRoute("/_layout/documents")({
    component: Documents,
});

export default Documents;
