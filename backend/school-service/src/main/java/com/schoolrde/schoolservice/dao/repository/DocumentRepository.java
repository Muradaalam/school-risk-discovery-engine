package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.DocumentEntity;

public interface DocumentRepository extends JpaRepository<DocumentEntity,Integer>{
		Optional<DocumentEntity> findById(Integer Id);

}