package com.schoolrde.schoolservice.config;
//SecurityConfig file is implemented with AI assistance 


/*
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig{

    @Bean 
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {

        http.csrf(csrf -> csrf.disable())
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .httpBasic(Customizer.withDefaults());
        return http.build();
    }
}*/


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;


@Configuration
public class SecurityConfig{

	private final JwtAuthenticationFilter jwtAuthenticationFilter;

	public SecurityConfig(JwtAuthenticationFilter jwtAuthenticationFilter){
	    this.jwtAuthenticationFilter = jwtAuthenticationFilter;
	}


	@Bean
	SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {

	    http.csrf(csrf -> csrf.disable()).sessionManagement(
	    		session ->session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
	    ).authorizeHttpRequests(auth -> auth
	            .requestMatchers("/school-service/auth/generateToken").permitAll()
	            .anyRequest().authenticated()
	    ).addFilterBefore(jwtAuthenticationFilter,UsernamePasswordAuthenticationFilter.class);

	    return http.build();
	}
}