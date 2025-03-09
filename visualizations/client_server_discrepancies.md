# Client/Server Test Pair Discrepancies

## Summary

| Proxy | Discrepancy Rate |
|-------|------------------|
| Caddy | 89.1% |
| Envoy | 73.4% |
| H2O | 65.6% |
| Apache | 50.0% |
| Nghttpx | 46.9% |
| Node | 46.9% |
| HAproxy | 45.3% |

## Most Common Discrepancy Types by Proxy

| Proxy | Most Common Discrepancy | Count | Percentage |
|-------|-------------------------|-------|------------|
| Nghttpx | dropped→reset | 24 | 80.0% |
| HAproxy | dropped→500 | 20 | 69.0% |
| Apache | dropped→500 | 26 | 81.2% |
| Caddy | goaway→500 | 22 | 38.6% |
| Node | dropped→other | 11 | 36.7% |
| Envoy | dropped→500 | 37 | 78.7% |
| H2O | goaway→dropped | 34 | 81.0% |

## Detailed Discrepancies

| Proxy | Test Pair | Client Result | Server Result | Discrepancy Type |
|-------|-----------|--------------|---------------|------------------|
| Caddy | C1/S106 | goaway | 500 | goaway→500 |
| H2O | C1/S106 | goaway | dropped | goaway→dropped |
| HAproxy | C7/S107 | dropped | 500 | dropped→500 |
| Caddy | C7/S107 | dropped | 500 | dropped→500 |
| H2O | C8/S108 | other | dropped | other→dropped |
| Nghttpx | C9/S109 | dropped | other | dropped→other |
| HAproxy | C9/S109 | dropped | 500 | dropped→500 |
| Apache | C9/S109 | dropped | 500 | dropped→500 |
| Caddy | C9/S109 | dropped | 500 | dropped→500 |
| Node | C9/S109 | dropped | other | dropped→other |
| Envoy | C9/S109 | dropped | 500 | dropped→500 |
| Nghttpx | C10/S110 | dropped | other | dropped→other |
| HAproxy | C10/S110 | 500 | other | 500→other |
| Caddy | C10/S110 | 500 | other | 500→other |
| Node | C10/S110 | dropped | other | dropped→other |
| Envoy | C10/S110 | 500 | dropped | 500→dropped |
| H2O | C10/S110 | other | dropped | other→dropped |
| Nghttpx | C15/S111 | goaway | dropped | goaway→dropped |
| Caddy | C15/S111 | goaway | 500 | goaway→500 |
| Envoy | C15/S111 | dropped | 500 | dropped→500 |
| H2O | C15/S111 | goaway | dropped | goaway→dropped |
| Caddy | C17/S112 | goaway | 500 | goaway→500 |
| Envoy | C17/S112 | dropped | 500 | dropped→500 |
| H2O | C17/S112 | goaway | dropped | goaway→dropped |
| Caddy | C18/S113 | goaway | 500 | goaway→500 |
| Caddy | C19/S114 | goaway | 500 | goaway→500 |
| H2O | C19/S114 | goaway | dropped | goaway→dropped |
| Caddy | C20/S115 | goaway | 500 | goaway→500 |
| Envoy | C20/S115 | dropped | 500 | dropped→500 |
| H2O | C20/S115 | goaway | dropped | goaway→dropped |
| Caddy | C21/S116 | goaway | 500 | goaway→500 |
| H2O | C21/S116 | goaway | dropped | goaway→dropped |
| Caddy | C25/S117 | goaway | 500 | goaway→500 |
| Envoy | C25/S117 | dropped | 500 | dropped→500 |
| H2O | C25/S117 | goaway | dropped | goaway→dropped |
| Caddy | C26/S118 | goaway | 500 | goaway→500 |
| Envoy | C26/S118 | dropped | 500 | dropped→500 |
| H2O | C26/S118 | goaway | dropped | goaway→dropped |
| HAproxy | C27/S119 | dropped | 500 | dropped→500 |
| Apache | C27/S119 | dropped | 500 | dropped→500 |
| Caddy | C27/S119 | dropped | 500 | dropped→500 |
| Envoy | C27/S119 | dropped | 500 | dropped→500 |
| Caddy | C30/S120 | goaway | 500 | goaway→500 |
| Envoy | C30/S120 | dropped | 500 | dropped→500 |
| H2O | C30/S120 | goaway | other | goaway→other |
| Caddy | C33/S121 | goaway | 500 | goaway→500 |
| Envoy | C33/S121 | dropped | 500 | dropped→500 |
| H2O | C33/S121 | goaway | dropped | goaway→dropped |
| Caddy | C34/S122 | goaway | 500 | goaway→500 |
| Node | C34/S122 | goaway | other | goaway→other |
| Envoy | C34/S122 | dropped | 500 | dropped→500 |
| H2O | C34/S122 | goaway | dropped | goaway→dropped |
| Caddy | C36/S124 | goaway | 500 | goaway→500 |
| H2O | C36/S124 | goaway | dropped | goaway→dropped |
| Caddy | C37/S125 | goaway | dropped | goaway→dropped |
| Node | C37/S125 | goaway | other | goaway→other |
| Envoy | C37/S125 | goaway | other | goaway→other |
| H2O | C37/S125 | goaway | dropped | goaway→dropped |
| HAproxy | C40/S126 | dropped | other | dropped→other |
| Apache | C40/S126 | dropped | goaway | dropped→goaway |
| H2O | C40/S126 | goaway | dropped | goaway→dropped |
| Nghttpx | C41/S127 | dropped | reset | dropped→reset |
| HAproxy | C41/S127 | dropped | 500 | dropped→500 |
| Apache | C41/S127 | dropped | 500 | dropped→500 |
| Caddy | C41/S127 | dropped | 500 | dropped→500 |
| Node | C41/S127 | dropped | 500 | dropped→500 |
| Envoy | C41/S127 | dropped | 500 | dropped→500 |
| H2O | C41/S127 | goaway | dropped | goaway→dropped |
| Nghttpx | C42/S128 | dropped | reset | dropped→reset |
| HAproxy | C42/S128 | goaway | 500 | goaway→500 |
| Apache | C42/S128 | dropped | 500 | dropped→500 |
| Caddy | C42/S128 | dropped | 500 | dropped→500 |
| Node | C42/S128 | dropped | other | dropped→other |
| Envoy | C42/S128 | dropped | 500 | dropped→500 |
| Nghttpx | C43/S129 | dropped | reset | dropped→reset |
| HAproxy | C43/S129 | dropped | 500 | dropped→500 |
| Apache | C43/S129 | dropped | 500 | dropped→500 |
| Caddy | C43/S129 | dropped | 500 | dropped→500 |
| Node | C43/S129 | dropped | other | dropped→other |
| Envoy | C43/S129 | dropped | 500 | dropped→500 |
| Nghttpx | C44/S130 | dropped | reset | dropped→reset |
| HAproxy | C44/S130 | dropped | 500 | dropped→500 |
| Apache | C44/S130 | dropped | 500 | dropped→500 |
| Caddy | C44/S130 | dropped | 500 | dropped→500 |
| Node | C44/S130 | dropped | other | dropped→other |
| Envoy | C44/S130 | dropped | 500 | dropped→500 |
| Nghttpx | C45/S131 | dropped | reset | dropped→reset |
| HAproxy | C45/S131 | dropped | 500 | dropped→500 |
| Apache | C45/S131 | dropped | 500 | dropped→500 |
| Caddy | C45/S131 | dropped | 500 | dropped→500 |
| Envoy | C45/S131 | dropped | 500 | dropped→500 |
| Nghttpx | C46/S132 | dropped | reset | dropped→reset |
| HAproxy | C46/S132 | dropped | 500 | dropped→500 |
| Apache | C46/S132 | dropped | 500 | dropped→500 |
| Caddy | C46/S132 | dropped | 500 | dropped→500 |
| Envoy | C46/S132 | dropped | 500 | dropped→500 |
| Nghttpx | C47/S133 | dropped | reset | dropped→reset |
| Apache | C47/S133 | dropped | 500 | dropped→500 |
| Caddy | C47/S133 | dropped | 500 | dropped→500 |
| Node | C47/S133 | dropped | other | dropped→other |
| Envoy | C47/S133 | dropped | 500 | dropped→500 |
| Nghttpx | C48/S134 | dropped | reset | dropped→reset |
| Apache | C48/S134 | dropped | 500 | dropped→500 |
| Caddy | C48/S134 | dropped | 500 | dropped→500 |
| Node | C48/S134 | dropped | other | dropped→other |
| Envoy | C48/S134 | dropped | 500 | dropped→500 |
| Nghttpx | C49/S135 | dropped | reset | dropped→reset |
| HAproxy | C49/S135 | 500 | dropped | 500→dropped |
| Caddy | C49/S135 | 500 | other | 500→other |
| Node | C49/S135 | dropped | other | dropped→other |
| Envoy | C49/S135 | 500 | other | 500→other |
| Nghttpx | C50/S136 | dropped | reset | dropped→reset |
| HAproxy | C50/S136 | 500 | dropped | 500→dropped |
| Caddy | C50/S136 | 500 | other | 500→other |
| Node | C50/S136 | dropped | other | dropped→other |
| Envoy | C50/S136 | 500 | other | 500→other |
| H2O | C50/S136 | dropped | other | dropped→other |
| Nghttpx | C51/S137 | dropped | reset | dropped→reset |
| HAproxy | C51/S137 | dropped | 500 | dropped→500 |
| Apache | C51/S137 | dropped | 500 | dropped→500 |
| Node | C51/S137 | dropped | 500 | dropped→500 |
| Envoy | C51/S137 | dropped | 500 | dropped→500 |
| H2O | C51/S137 | goaway | dropped | goaway→dropped |
| Nghttpx | C52/S138 | dropped | reset | dropped→reset |
| HAproxy | C52/S138 | dropped | 500 | dropped→500 |
| Apache | C52/S138 | dropped | 500 | dropped→500 |
| Caddy | C52/S138 | dropped | other | dropped→other |
| Node | C52/S138 | dropped | 500 | dropped→500 |
| Envoy | C52/S138 | dropped | 500 | dropped→500 |
| Nghttpx | C53/S139 | dropped | reset | dropped→reset |
| HAproxy | C53/S139 | dropped | 500 | dropped→500 |
| Apache | C53/S139 | dropped | 500 | dropped→500 |
| Caddy | C53/S139 | dropped | other | dropped→other |
| Node | C53/S139 | dropped | 500 | dropped→500 |
| Envoy | C53/S139 | dropped | 500 | dropped→500 |
| Nghttpx | C54/S140 | dropped | reset | dropped→reset |
| HAproxy | C54/S140 | dropped | 500 | dropped→500 |
| Apache | C54/S140 | dropped | 500 | dropped→500 |
| Caddy | C54/S140 | dropped | other | dropped→other |
| Node | C54/S140 | dropped | 500 | dropped→500 |
| Envoy | C54/S140 | dropped | 500 | dropped→500 |
| H2O | C54/S140 | goaway | dropped | goaway→dropped |
| Nghttpx | C55/S141 | dropped | reset | dropped→reset |
| HAproxy | C55/S141 | dropped | 500 | dropped→500 |
| Apache | C55/S141 | dropped | 500 | dropped→500 |
| Caddy | C55/S141 | dropped | other | dropped→other |
| Node | C55/S141 | dropped | 500 | dropped→500 |
| Envoy | C55/S141 | dropped | 500 | dropped→500 |
| H2O | C55/S141 | other | dropped | other→dropped |
| Nghttpx | C56/S142 | dropped | reset | dropped→reset |
| Apache | C56/S142 | dropped | 500 | dropped→500 |
| Caddy | C56/S142 | dropped | other | dropped→other |
| Node | C56/S142 | dropped | 500 | dropped→500 |
| Envoy | C56/S142 | dropped | 500 | dropped→500 |
| H2O | C56/S142 | goaway | dropped | goaway→dropped |
| Nghttpx | C57/S143 | dropped | reset | dropped→reset |
| HAproxy | C57/S143 | dropped | 500 | dropped→500 |
| Apache | C57/S143 | dropped | 500 | dropped→500 |
| Caddy | C57/S143 | dropped | 500 | dropped→500 |
| Node | C57/S143 | dropped | 500 | dropped→500 |
| Envoy | C57/S143 | dropped | 500 | dropped→500 |
| H2O | C57/S143 | goaway | dropped | goaway→dropped |
| Nghttpx | C60/S61 | dropped | reset | dropped→reset |
| HAproxy | C60/S61 | dropped | 500 | dropped→500 |
| Apache | C60/S61 | dropped | 500 | dropped→500 |
| Caddy | C60/S61 | dropped | 500 | dropped→500 |
| Node | C60/S61 | dropped | 500 | dropped→500 |
| Envoy | C60/S61 | dropped | 500 | dropped→500 |
| H2O | C60/S61 | goaway | dropped | goaway→dropped |
| Nghttpx | C58/S59 | reset | dropped | reset→dropped |
| HAproxy | C58/S59 | 500 | dropped | 500→dropped |
| Apache | C58/S59 | 500 | dropped | 500→dropped |
| Caddy | C58/S59 | 500 | dropped | 500→dropped |
| Node | C58/S59 | 500 | dropped | 500→dropped |
| Envoy | C58/S59 | 500 | dropped | 500→dropped |
| H2O | C58/S59 | dropped | goaway | dropped→goaway |
| Nghttpx | C62/S64 | dropped | reset | dropped→reset |
| HAproxy | C62/S64 | dropped | 500 | dropped→500 |
| Apache | C62/S64 | dropped | 500 | dropped→500 |
| Caddy | C62/S64 | dropped | 500 | dropped→500 |
| Node | C62/S64 | dropped | 500 | dropped→500 |
| Envoy | C62/S64 | dropped | 500 | dropped→500 |
| H2O | C62/S64 | goaway | dropped | goaway→dropped |
| Nghttpx | C63/S65 | dropped | reset | dropped→reset |
| HAproxy | C63/S65 | dropped | 500 | dropped→500 |
| Apache | C63/S65 | dropped | 500 | dropped→500 |
| Caddy | C63/S65 | dropped | 500 | dropped→500 |
| Node | C63/S65 | dropped | 500 | dropped→500 |
| Envoy | C63/S65 | dropped | 500 | dropped→500 |
| H2O | C63/S65 | goaway | dropped | goaway→dropped |
| HAproxy | C76/S144 | goaway | dropped | goaway→dropped |
| Caddy | C76/S144 | goaway | dropped | goaway→dropped |
| H2O | C76/S144 | goaway | dropped | goaway→dropped |
| Caddy | C77/S145 | goaway | 500 | goaway→500 |
| Envoy | C77/S145 | dropped | 500 | dropped→500 |
| H2O | C77/S145 | goaway | dropped | goaway→dropped |
| Caddy | C78/S146 | goaway | 500 | goaway→500 |
| Envoy | C78/S146 | dropped | 500 | dropped→500 |
| H2O | C78/S146 | goaway | dropped | goaway→dropped |
| Nghttpx | C79/S147 | dropped | other | dropped→other |
| HAproxy | C79/S147 | dropped | 500 | dropped→500 |
| Apache | C79/S147 | dropped | 500 | dropped→500 |
| Caddy | C79/S147 | other | 500 | other→500 |
| Node | C79/S147 | dropped | other | dropped→other |
| Envoy | C79/S147 | dropped | 500 | dropped→500 |
| Caddy | C80/S148 | goaway | 500 | goaway→500 |
| H2O | C80/S148 | goaway | dropped | goaway→dropped |
| Caddy | C81/S149 | goaway | dropped | goaway→dropped |
| H2O | C81/S149 | goaway | dropped | goaway→dropped |
| Caddy | C82/S150 | goaway | 500 | goaway→500 |
| Envoy | C82/S150 | goaway | other | goaway→other |
| H2O | C82/S150 | goaway | dropped | goaway→dropped |
| Nghttpx | C83/S151 | goaway | other | goaway→other |
| HAproxy | C83/S151 | dropped | other | dropped→other |
| Apache | C83/S151 | goaway | other | goaway→other |
| Caddy | C83/S151 | dropped | other | dropped→other |
| Node | C83/S151 | goaway | other | goaway→other |
| Envoy | C83/S151 | goaway | other | goaway→other |
| HAproxy | C84/S152 | dropped | 500 | dropped→500 |
| Apache | C84/S152 | dropped | goaway | dropped→goaway |
| Caddy | C84/S152 | dropped | 500 | dropped→500 |
| Envoy | C84/S152 | dropped | other | dropped→other |
| Caddy | C85/S153 | goaway | 500 | goaway→500 |
| Node | C85/S153 | other | goaway | other→goaway |
| H2O | C85/S153 | goaway | dropped | goaway→dropped |
| Caddy | C86/S154 | goaway | 500 | goaway→500 |
| Envoy | C86/S154 | dropped | 500 | dropped→500 |
| H2O | C86/S154 | goaway | dropped | goaway→dropped |
| HAproxy | C88/S155 | dropped | 500 | dropped→500 |
| Apache | C88/S155 | dropped | 500 | dropped→500 |
| Caddy | C88/S155 | dropped | 500 | dropped→500 |
| Envoy | C88/S155 | dropped | 500 | dropped→500 |
| Node | C93/S156 | dropped | other | dropped→other |
| Caddy | C94/S157 | goaway | 500 | goaway→500 |
| Node | C94/S157 | goaway | dropped | goaway→dropped |
| H2O | C94/S157 | goaway | dropped | goaway→dropped |
| Caddy | C95/S158 | goaway | 500 | goaway→500 |
| Node | C95/S158 | goaway | dropped | goaway→dropped |
| Envoy | C95/S158 | goaway | other | goaway→other |
| H2O | C95/S158 | goaway | dropped | goaway→dropped |
| Caddy | C96/S159 | goaway | 500 | goaway→500 |
| Node | C96/S159 | goaway | dropped | goaway→dropped |
| Envoy | C96/S159 | goaway | other | goaway→other |
| H2O | C96/S159 | goaway | dropped | goaway→dropped |
| Apache | C97/S160 | dropped | goaway | dropped→goaway |
| H2O | C97/S160 | goaway | dropped | goaway→dropped |
| Nghttpx | C98/S161 | dropped | reset | dropped→reset |
| Apache | C98/S161 | dropped | 500 | dropped→500 |
| Caddy | C98/S161 | dropped | 500 | dropped→500 |
| Envoy | C98/S161 | dropped | 500 | dropped→500 |
| Nghttpx | C99/S162 | dropped | reset | dropped→reset |
| Apache | C99/S162 | dropped | 500 | dropped→500 |
| Caddy | C99/S162 | dropped | 500 | dropped→500 |
| Envoy | C99/S162 | dropped | 500 | dropped→500 |
| H2O | C99/S162 | other | dropped | other→dropped |
| Nghttpx | C100/S163 | dropped | reset | dropped→reset |
| Apache | C100/S163 | dropped | 500 | dropped→500 |
| Caddy | C100/S163 | dropped | 500 | dropped→500 |
| Envoy | C100/S163 | dropped | 500 | dropped→500 |
| H2O | C100/S163 | other | dropped | other→dropped |
| Nghttpx | C101/S164 | dropped | reset | dropped→reset |
| Apache | C101/S164 | dropped | 500 | dropped→500 |
| Caddy | C101/S164 | dropped | 500 | dropped→500 |
| Envoy | C101/S164 | dropped | 500 | dropped→500 |
| HAproxy | C102/S165 | dropped | other | dropped→other |
| Apache | C102/S165 | dropped | goaway | dropped→goaway |
| H2O | C102/S165 | goaway | dropped | goaway→dropped |
