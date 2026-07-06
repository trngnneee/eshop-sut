# Traceability Matrix - State Transition Testing FR-10

## FR-10 - Trạng thái Đơn hàng (Order State Machine)

| Requirement ID | Test Case ID | Technique | Coverage Item | Source | Result | Related Bug |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FR-10 | [FR10-S-TC01](../test-cases/order_state_machine/FR10-S-TC01.md) | State Transition Testing | S-VALID-01 - Valid FR-10 transition; actor is allowed for this action. | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC02](../test-cases/order_state_machine/FR10-S-TC02.md) | State Transition Testing | S-VALID-02 - Valid FR-10 transition; actor is allowed for this action. | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC03](../test-cases/order_state_machine/FR10-S-TC03.md) | State Transition Testing | S-VALID-03 - Valid FR-10 transition; actor is allowed for this action. | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC04](../test-cases/order_state_machine/FR10-S-TC04.md) | State Transition Testing | S-VALID-04 - Valid FR-10 transition; actor is allowed for this action. | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC05](../test-cases/order_state_machine/FR10-S-TC05.md) | State Transition Testing | S-VALID-05 - Valid FR-10 transition; actor is allowed for this action. | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC06](../test-cases/order_state_machine/FR10-S-TC06.md) | State Transition Testing | S-VALID-06 - Valid FR-10 transition; actor is allowed for this action. | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC07](../test-cases/order_state_machine/FR10-S-TC07.md) | State Transition Testing | S-VALID-07 - Valid FR-10 transition; actor is allowed for this action. | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC08](../test-cases/order_state_machine/FR10-S-TC08.md) | State Transition Testing | S-INVALID-01 - Invalid transition: pending -> shipping skips confirmed | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC09](../test-cases/order_state_machine/FR10-S-TC09.md) | State Transition Testing | S-INVALID-02 - Invalid transition: confirmed -> delivered skips shipping | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC10](../test-cases/order_state_machine/FR10-S-TC10.md) | State Transition Testing | S-INVALID-03 - Invalid transition: shipping -> confirmed | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC11](../test-cases/order_state_machine/FR10-S-TC11.md) | State Transition Testing | S-INVALID-04 - Invalid transition: shipping -> canceled | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC12](../test-cases/order_state_machine/FR10-S-TC12.md) | State Transition Testing | S-INVALID-05 - Invalid transition: user cannot cancel shipping order | README.md:141-162; api_specification.md:173-182 | Failed | BUG-FR10-S-01 - User có thể hủy đơn hàng đang shipping |
| FR-10 | [FR10-S-TC13](../test-cases/order_state_machine/FR10-S-TC13.md) | State Transition Testing | S-INVALID-06 - Invalid final-state transition: delivered -> canceled by user | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC14](../test-cases/order_state_machine/FR10-S-TC14.md) | State Transition Testing | S-INVALID-07 - Invalid final-state transition: canceled remains final for user | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC15](../test-cases/order_state_machine/FR10-S-TC15.md) | State Transition Testing | S-INVALID-08 - Invalid final-state transition: delivered -> canceled by admin | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC16](../test-cases/order_state_machine/FR10-S-TC16.md) | State Transition Testing | S-INVALID-09 - Invalid final-state transition: canceled -> delivered by admin | README.md:141-162; api_specification.md:173-182 | Failed | BUG-FR10-S-02 - Admin có thể chuyển final state canceled sang delivered |
| FR-10 | [FR10-S-TC17](../test-cases/order_state_machine/FR10-S-TC17.md) | State Transition Testing | S-INVALID-10 - Invalid transition: no-op status update pending -> pending | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC18](../test-cases/order_state_machine/FR10-S-TC18.md) | State Transition Testing | S-INVALID-11 - Invalid status value: refund | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC19](../test-cases/order_state_machine/FR10-S-TC19.md) | State Transition Testing | S-INVALID-12 - Invalid status value: empty string | README.md:141-162; api_specification.md:173-182 | Passed | None |
| FR-10 | [FR10-S-TC20](../test-cases/order_state_machine/FR10-S-TC20.md) | State Transition Testing | S-INVALID-13 - Invalid status value: null | README.md:141-162; api_specification.md:173-182 | Passed | None |
