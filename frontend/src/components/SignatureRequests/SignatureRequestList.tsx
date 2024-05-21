import { fetchSignatureRequests } from "../../client/services/SignatureRequestsService";
import {
  Container,
  Flex,
  Heading,
  Spinner,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { useQuery } from "react-query";
import { type ApiError } from "../../client";
import ActionsMenu from "../Common/ActionsMenu";
import Navbar from "../Common/Navbar";
import useCustomToast from "../../hooks/useCustomToast";

const SignatureRequestList = () => {
  const showToast = useCustomToast();
  const {
    data: signatureRequests,
    isLoading,
    isError,
    error,
  } = useQuery("signatureRequests", fetchSignatureRequests);

  if (isError) {
    const errDetail = (error as ApiError).body?.detail;
    showToast("Something went wrong.", `${errDetail}`, "error");
  }

  return (
    <>
      {isLoading ? (
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color="ui.main" />
        </Flex>
      ) : (
        signatureRequests && (
          <Container maxW="full">
            <Heading
              size="lg"
              textAlign={{ base: "center", md: "left" }}
              pt={12}
            >
              Signature Requests Management
            </Heading>
            <Navbar type={"Request"} />
            <TableContainer>
              <Table size={{ base: "sm", md: "md" }}>
                <Thead>
                  <Tr>
                    <Th>ID</Th>
                    <Th>Name</Th>
                    <Th>Delivery Mode</Th>
                    <Th>Expiration Date</Th>
                    <Th>Actions</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {signatureRequests.map((request) => (
                    <Tr key={request.id}>
                      <Td>{request.id}</Td>
                      <Td>{request.name}</Td>
                      <Td>{request.delivery_mode}</Td>
                      <Td>{request.expiration_date || "N/A"}</Td>
                      <Td>
                        <ActionsMenu type={"SignatureRequest"} value={request} />
                      </Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </Container>
        )
      )}
    </>
  );
};

export default SignatureRequestList;
