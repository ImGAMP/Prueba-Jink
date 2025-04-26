package com.productos.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;

@Configuration
public class SecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health", "/actuator/info").permitAll() // Deja pasar health sin auth
                .anyRequest().authenticated() // Todo lo demás sigue protegido
            )
            .csrf(csrf -> csrf.disable()) // (opcional para APIs sin formulario)
            .build();
    }
}
