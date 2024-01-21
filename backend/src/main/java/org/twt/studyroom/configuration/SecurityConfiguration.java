package org.twt.studyroom.configuration;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfiguration {
    @Bean
    PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf(AbstractHttpConfigurer::disable)
                .sessionManagement(
                        session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                );

        http.logout(AbstractHttpConfigurer::disable);

        http.authorizeHttpRequests(
                auth -> auth.requestMatchers(
                                "/**"
                        ).permitAll()
                        .anyRequest().authenticated()
        );

        http.exceptionHandling(
                handle -> handle
                        .accessDeniedHandler(
                                (request, response, accessDeniedException) -> {
                                    response.getWriter().println("{\"code\":403,\"message\":\"Forbidden\"}");
                                    response.setHeader("Content-Type", "application/json;charset=utf-8");
                                    response.setStatus(HttpServletResponse.SC_FORBIDDEN);
                                }
                        )
                        .authenticationEntryPoint(
                                (request, response, authException) -> {
                                    response.getWriter().println("{\"code\":401,\"message\":\"Unauthorized\"}");
                                    response.setHeader("Content-Type", "application/json;charset=utf-8");
                                    response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                                }
                        )
        );

        return http.build();
    }
}
