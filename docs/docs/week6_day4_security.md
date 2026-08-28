# Week 6 Day 4 - Agent Security & Permission

## 1. Goal

为电商客服Agent增加输入安全、
Tool权限、Action控制和敏感信息脱敏。

## 2. Input Guard

测试正常输入和Prompt Injection。

## 3. Tool Permission

Tool按照LOW、MEDIUM、ACTION进行风险分级。

## 4. Action Guard

transfer_to_human必须存在明确用户意图。

## 5. Output Masking

手机号、邮箱等敏感信息输出前进行脱敏。

## 6. Security Metrics

- blocked_requests
- permission_denied
- security_events
- masked_count

## 7. Bad Cases

- Prompt Injection
- System Prompt Leakage
- Privilege Escalation
- Unauthorized Tool Call
- Sensitive Data Leakage
- Cross-user Data Access

## 8. Limitations

当前Input Guard主要基于规则，
只能作为基础防护。

当前Demo尚未实现真实用户身份认证和订单所有权校验。

## 9. Conclusion

完成Agent输入、Tool执行和输出三个阶段的基础安全控制。