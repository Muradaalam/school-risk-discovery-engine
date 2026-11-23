package com.schoolrde.schoolservice.dao.repository;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.entity.SchoolEntireEntity;

public interface SchoolRepository extends JpaRepository<SchoolEntity,Long>{
    Optional<SchoolEntity> findBySchoolId(String schoolId);
    
    @Query("SELECT s FROM SchoolEntireEntity s WHERE s.id = :id")
    Optional<SchoolEntireEntity> findById(@Param("id") Integer id);
    
    boolean existsBySchoolId(String schoolId);
    void deleteBySchoolId(String schoolId);
    
    @Query(value = """
            SELECT s.* FROM school s INNER JOIN priority_snapshot ps ON ps.school_id = s.id 
            WHERE ps.id = (
            	SELECT ps2.id FROM priority_snapshot ps2 
            	WHERE ps2.school_id = s.id ORDER BY ps2.snapshot_date DESC, ps2.id DESC LIMIT 1
            )
            ORDER BY ps.priority_score DESC, s.id ASC LIMIT 50
            """, nativeQuery = true)
        List<SchoolEntireEntity> findTop50SchoolsByPriorityScore();

    @Query(value = """
        SELECT s.*
        FROM school s
        LEFT JOIN priority_snapshot ps
          ON ps.id = (
            SELECT ps2.id
            FROM priority_snapshot ps2
            WHERE ps2.school_id = s.id
            ORDER BY ps2.snapshot_date DESC, ps2.id DESC
            LIMIT 1
          )
        WHERE (
          :query = ''
          OR LOWER(s.school_name) LIKE LOWER(CONCAT('%', :query, '%'))
          OR LOWER(s.school_id) LIKE LOWER(CONCAT('%', :query, '%'))
          OR LOWER(s.udise_code) LIKE LOWER(CONCAT('%', :query, '%'))
          OR LOWER(s.district) LIKE LOWER(CONCAT('%', :query, '%'))
          OR CAST(s.id AS CHAR) LIKE CONCAT('%', :query, '%')
        )
        AND (
          :priorityScore IS NULL
          OR ps.priority_score = :priorityScore
        )
        ORDER BY
          CASE WHEN ps.priority_score IS NULL THEN 1 ELSE 0 END,
          ps.priority_score DESC,
          s.id ASC
        LIMIT 100
        """, nativeQuery = true)
    List<SchoolEntireEntity> searchSchools(
        @Param("query") String query,
        @Param("priorityScore") Integer priorityScore
    );

    
}