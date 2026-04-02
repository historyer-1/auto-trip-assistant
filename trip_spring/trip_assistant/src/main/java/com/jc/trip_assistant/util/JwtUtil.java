package com.jc.trip_assistant.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Date;
import java.util.Map;

/**
 * JWT工具类，负责令牌生成与解析。
 */
@Component
public class JwtUtil {

    /**
     * JWT密钥配置。
     */
    @Value("${jwt.secret}")
    private String secret;

    /**
     * JWT过期时间（分钟）。
     */
    @Value("${jwt.expire-minutes}")
    private long expireMinutes;

    /**
     * 生成JWT令牌。
     *
     * @param claims 业务载荷数据
     * @return 生成后的JWT字符串
     */
    public String generateToken(Map<String, Object> claims) {
        // 构建签名密钥，统一采用HMAC-SHA算法。
        SecretKey key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        // 计算签发时间与过期时间，保证令牌时效性。
        Instant now = Instant.now();
        Instant expireAt = now.plus(expireMinutes, ChronoUnit.MINUTES);
        // 基于业务载荷构建并签发JWT。
        return Jwts.builder()
                .setClaims(claims)
                .setIssuedAt(Date.from(now))
                .setExpiration(Date.from(expireAt))
                .signWith(key)
                .compact();
    }

    /**
     * 解析JWT令牌。
     *
     * @param token JWT字符串
     * @return JWT声明数据
     */
    public Claims parseToken(String token) {
        // 使用同一密钥进行签名校验和载荷解析。
        SecretKey key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        Jws<Claims> claimsJws = Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token);
        // 返回令牌中的业务声明供调用方使用。
        return claimsJws.getBody();
    }
}
